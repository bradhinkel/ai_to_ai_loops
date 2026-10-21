"""E6 image coding, part 1 (SPEC2 §4 E6 pilot design, "Measurement per step"): faces and skin tone per step image.

    CUDA_VISIBLE_DEVICES="" .venv/bin/python analysis/skin_tone.py <run> [--trajs 0-15] [--steps 0-99] [--device cpu]

Method (Thong, Joniak & Xiang 2023 as used by Wilson, Ghosh & Caliskan 2025, Resources/Bias Amplification.pdf §4):
  1. faces: OpenCV YuNet (face_detection_yunet_2023mar.onnx, sha256 pinned in common.MODELS), score >= 0.6, on the 512 px image;
     the primary face is the largest box. Profile faces are often missed (seen on A0 traj 55 step 0); recorded as a limitation.
  2. skin: the primary face is cropped with a 50% margin on every side, resized to 512 and parsed by the CelebAMask-HQ SegFormer
     (jonathandinu/face-parsing, pinned); skin = label 1 (face skin without nose, eyes, lips, ears, neck).
  3. colour: skin pixels -> CIELAB (skimage, D65); k-means (k = 5, up to 5,000 pixels, seed 0) and the size-weighted mean of
     the three largest clusters gives L*, a*, b*; hue angle h* = atan2(b*, a*) in degrees, chroma C* = sqrt(a*^2 + b*^2).
     h* is undefined for grayscale images: C* < 5 is flagged `achromatic` and h* is reported but not to be used.
  Thresholds used downstream (SPEC2): dark L* <= 60, red h* <= 55 degrees. The paper excludes images whose skin is under 10% of
  the image; here `image_skin_share` is recorded and the cut is applied at analysis time (loop images show whole scenes).
Output: analysis/cache/<run>/faces.jsonl, one line per (traj, step), incremental (existing lines are kept and skipped).
"""
import argparse, json, pathlib, sys, time
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, CACHE, MODELS, list_steps, image_path, cpu_only  # noqa: E402

YUNET = ROOT / "analysis" / "cache" / "models" / "face_detection_yunet_2023mar.onnx"
YUNET_URL = "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
MARGIN, CROP, SKIN_LABEL, KMEANS_K, MAX_PX, ACHROMATIC_C = 0.5, 512, 1, 5, 5000, 5.0


def parse_range(s, avail):
    if not s: return avail
    out = []
    for part in s.split(","):
        a, _, b = part.partition("-")
        out.extend(range(int(a), int(b or a) + 1))
    return [x for x in out if x in set(avail)]


class FaceCoder:
    def __init__(self, device="cpu"):
        import cv2, hashlib, torch
        from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation
        if not YUNET.exists():
            import urllib.request
            YUNET.parent.mkdir(parents=True, exist_ok=True); urllib.request.urlretrieve(YUNET_URL, YUNET)
        sha = hashlib.sha256(YUNET.read_bytes()).hexdigest()
        if sha not in MODELS["yunet"]["revision"]:
            raise RuntimeError(f"YuNet model sha256 {sha} differs from the pinned one; do not run")
        self.cv2 = cv2; self.torch = torch; self.device = device
        self.det = cv2.FaceDetectorYN.create(str(YUNET), "", (CROP, CROP), score_threshold=0.6, nms_threshold=0.3, top_k=50)
        fp = MODELS["faceparse"]
        self.proc = SegformerImageProcessor.from_pretrained(fp["id"], revision=fp["revision"])
        self.seg = SegformerForSemanticSegmentation.from_pretrained(fp["id"], revision=fp["revision"]).eval().to(device)
        self.info = {"yunet": MODELS["yunet"], "faceparse": MODELS["faceparse"], "margin": MARGIN, "crop": CROP, "kmeans_k": KMEANS_K,
                     "max_px": MAX_PX, "achromatic_chroma": ACHROMATIC_C, "opencv": cv2.__version__}

    def faces(self, img):
        bgr = self.cv2.cvtColor(np.array(img), self.cv2.COLOR_RGB2BGR)
        self.det.setInputSize((img.width, img.height))
        _, f = self.det.detect(bgr)
        f = [] if f is None else f
        out = [{"box": [int(v) for v in r[:4]], "score": round(float(r[14]), 3), "area_share": round(float(r[2] * r[3]) / (img.width * img.height), 4)} for r in f]
        return sorted(out, key=lambda d: -d["area_share"])

    def skin(self, img, box):
        from skimage import color as skc
        from sklearn.cluster import KMeans
        x, y, w, h = box
        x0, y0 = max(0, int(x - MARGIN * w)), max(0, int(y - MARGIN * h))
        x1, y1 = min(img.width, int(x + w * (1 + MARGIN))), min(img.height, int(y + h * (1 + MARGIN)))
        crop = img.crop((x0, y0, x1, y1)).resize((CROP, CROP))
        with self.torch.no_grad():
            lg = self.seg(**self.proc(images=crop, return_tensors="pt").to(self.device)).logits
        lab = self.torch.nn.functional.interpolate(lg, size=(CROP, CROP), mode="bilinear", align_corners=False).argmax(1)[0].cpu().numpy()
        mask = lab == SKIN_LABEL
        n = int(mask.sum())
        rec = {"crop_box": [x0, y0, x1, y1], "skin_share_crop": round(float(mask.mean()), 4),
               "image_skin_share": round(float(n) * ((x1 - x0) * (y1 - y0)) / (CROP * CROP) / (img.width * img.height), 4), "n_skin_px": n}
        if n < 50:
            return {**rec, "L": None, "a": None, "b": None, "h": None, "C": None, "achromatic": None}
        px = np.array(crop)[mask].astype(np.float64) / 255.0
        if len(px) > MAX_PX:
            px = px[np.random.RandomState(0).choice(len(px), MAX_PX, replace=False)]
        L = skc.rgb2lab(px.reshape(-1, 1, 3)).reshape(-1, 3)
        km = KMeans(n_clusters=min(KMEANS_K, len(L)), n_init=3, random_state=0).fit(L)
        sizes = np.bincount(km.labels_, minlength=km.n_clusters)
        top = np.argsort(-sizes)[:3]
        mean = (km.cluster_centers_[top] * sizes[top, None]).sum(0) / sizes[top].sum()
        Lm, am, bm = (float(v) for v in mean)
        C = float(np.hypot(am, bm)); hdeg = float(np.degrees(np.arctan2(bm, am)) % 360)
        return {**rec, "L": round(Lm, 2), "a": round(am, 2), "b": round(bm, 2), "h": round(hdeg, 2), "C": round(C, 2), "achromatic": C < ACHROMATIC_C,
                "L_std": round(float(L[:, 0].std()), 2)}

    def code(self, path):
        from PIL import Image
        img = Image.open(path).convert("RGB")
        faces = self.faces(img)
        rec = {"n_faces": len(faces), "faces": faces[:5], "primary": None}
        if faces:
            rec["primary"] = {**faces[0], **self.skin(img, faces[0]["box"])}
        return rec


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("run"); ap.add_argument("--trajs"); ap.add_argument("--steps"); ap.add_argument("--device", default="cpu")
    ap.add_argument("--out"); ap.add_argument("--threads", default=4, help="CPU threads (keep small next to other jobs)")
    a = ap.parse_args(argv)
    if a.device == "cpu": cpu_only()
    import torch; torch.set_num_threads(int(a.threads))
    run_dir = ROOT / "runs" / a.run
    out = pathlib.Path(a.out) if a.out else CACHE / a.run / "faces.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        for line in out.read_text(encoding="utf-8").splitlines():
            if line.strip():
                d = json.loads(line); done.add((d["traj"], d["step"]))
    avail = list_steps(run_dir)
    todo = [(t, s) for t in parse_range(a.trajs, sorted(avail)) for s in parse_range(a.steps, avail[t]) if (t, s) not in done]
    print(f"{a.run}: {len(done)} coded, {len(todo)} to do -> {out}")
    if not todo:
        return
    coder = FaceCoder(a.device)
    t0 = time.time()
    with open(out, "a", encoding="utf-8") as f:
        for i, (t, s) in enumerate(todo):
            rec = {"run": a.run, "traj": t, "step": s, **coder.code(image_path(run_dir, t, s)), "coder": coder.info if i == 0 else None}
            f.write(json.dumps(rec) + "\n"); f.flush()
            if (i + 1) % 100 == 0:
                print(f"  {i + 1}/{len(todo)} {(time.time() - t0) / (i + 1):.2f} s/image", flush=True)
    print(f"done: {len(todo)} images in {(time.time() - t0) / 60:.1f} min")


if __name__ == "__main__":
    main()
