"""Append-only, crash-safe per-step records.

runs/<run>/traj_<TTT>/step_<NNN>.png       image k (512x512 PNG, as Hintze saved it)
runs/<run>/traj_<TTT>/step_<NNN>.gen.json  generation record, written right after the image (pass 1)
runs/<run>/traj_<TTT>/step_<NNN>.json      full record incl. caption; its presence means step k is complete (pass 2)

Every file is written to a .tmp sibling, fsynced and renamed, so a power cut leaves either nothing or a whole file.
Nothing under runs/ is ever overwritten: an orphan image without its gen.json (crash between the two renames)
is moved aside as .orphan-<ts>.png before being regenerated.
"""
import hashlib, io, json, os, pathlib, time


def atomic_write_bytes(path, data: bytes):
    path = pathlib.Path(path)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def atomic_write_json(path, obj):
    atomic_write_bytes(path, (json.dumps(obj, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))


def append_jsonl(path, obj):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sha256_bytes(b: bytes):
    return hashlib.sha256(b).hexdigest()


class TrajStore:
    def __init__(self, run_dir, traj: int, seed_prompt: str):
        self.traj = traj
        self.seed_prompt = seed_prompt
        self.dir = pathlib.Path(run_dir) / f"traj_{traj:03d}"
        self.dir.mkdir(parents=True, exist_ok=True)
        for tmp in self.dir.glob("*.tmp"):   # leftovers of an interrupted write; never data
            tmp.unlink()

    # paths
    def png(self, step):  return self.dir / f"step_{step:03d}.png"
    def gen(self, step):  return self.dir / f"step_{step:03d}.gen.json"
    def rec(self, step):  return self.dir / f"step_{step:03d}.json"

    # state
    def is_complete(self, step):  return self.rec(step).exists()
    def has_image(self, step):
        if self.gen(step).exists() and self.png(step).exists():
            return True
        if self.png(step).exists():      # orphan: image without its record
            self.png(step).rename(self.dir / f"step_{step:03d}.orphan-{int(time.time())}.png")
        return False

    def last_complete_step(self):
        steps = sorted(int(p.stem.split("_")[1]) for p in self.dir.glob("step_???.json"))
        last = -1
        for s in steps:                   # first gap counts as the end
            if s != last + 1:
                break
            last = s
        return last

    def prompt_for(self, step):
        """Prompt that makes image `step`: the seed for step 0, else the caption of image step-1."""
        if step == 0:
            return self.seed_prompt, "seed"
        prev = read_json(self.rec(step - 1))
        return prev["caption"], f"caption_of_step_{step-1:03d}"

    def captions_for(self, step):
        """Candidate prompts for image `step` (Part 2, K > 1): the K captions of image step-1; [seed] at step 0."""
        if step == 0:
            return [self.seed_prompt], "seed"
        prev = read_json(self.rec(step - 1))
        caps = prev.get("captions") or [prev["caption"]]
        return caps, f"captions_of_step_{step-1:03d}"

    # candidates (Part 2): step_NNN.c<round>_<k>.png next to the chosen step_NNN.png
    def cand_png(self, step, round_, k):  return self.dir / f"step_{step:03d}.c{round_}_{k}.png"
    def clear_candidates(self, step):
        """Leftover candidates of an interrupted step are moved aside, never overwritten."""
        for p in self.dir.glob(f"step_{step:03d}.c*_*.png"):
            if ".orphan-" not in p.name:
                p.rename(self.dir / (p.stem + f".orphan-{int(time.time())}.png"))
    def write_candidate(self, step, round_, k, image):
        buf = io.BytesIO(); image.save(buf, format="PNG", optimize=True); data = buf.getvalue()
        atomic_write_bytes(self.cand_png(step, round_, k), data)
        return {"file": self.cand_png(step, round_, k).name, "sha256": sha256_bytes(data)}

    # writes
    def write_image(self, step, image, gen_record: dict):
        buf = io.BytesIO()
        image.save(buf, format="PNG", optimize=True)     # as in the OSF code
        data = buf.getvalue()
        gen_record = dict(gen_record, image=self.png(step).name, image_sha256=sha256_bytes(data), image_bytes=len(data))
        atomic_write_bytes(self.png(step), data)
        atomic_write_json(self.gen(step), gen_record)
        return gen_record

    def write_record(self, step, record: dict):
        atomic_write_json(self.rec(step), record)
