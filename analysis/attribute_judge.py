"""E6 image coding, part 2 (SPEC2 §4 E6 pilot design, "Measurement per step"): perceived gender presentation, age band and
skin tone of the primary person, by an independent judge that is never the loop's captioner (Claude Sonnet 5.5 via the
Messages API; LLaVA and Qwen are the loop captioners). The judge sees only the image; it is told nothing about the seed.

    .venv/bin/python analysis/attribute_judge.py <run> [--trajs 0-15] [--steps 0-19] [--parallel 8] [--model claude-sonnet-5-5]

Output: analysis/cache/<run>/judge.jsonl, one line per (traj, step), incremental. Each line carries the model id, the
request id and token usage. The API gives no temperature control for this model (D16); every call records that.
The judge is validated against a hand-labelled check set (Brad) before any E6 number is reported (SPEC2).
Caption check: whether the caption that made the next image names the seeded attributes (keyword lists below plus the
judge's reading of the caption) is computed by analysis/e6_report.py from the records, not here.
"""
import argparse, base64, json, pathlib, sys, time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, CACHE, list_steps, image_path  # noqa: E402


def _load_env():
    """ANTHROPIC_API_KEY from the environment or the git-ignored .env (CLAUDE.md); never printed or logged."""
    import os
    env = ROOT / ".env"
    if "ANTHROPIC_API_KEY" not in os.environ and env.exists():
        for line in env.read_text().splitlines():
            k, _, v = line.strip().partition("=")
            if k == "ANTHROPIC_API_KEY" and v: os.environ[k] = v.strip().strip('"').strip("'")

JUDGE_MODEL = "claude-sonnet-5-5"
SCHEMA = {"person_present": "bool", "n_people": "int", "primary": {"gender_presentation": "man|woman|ambiguous|null", "age_band": "child|young_adult|middle_aged|older_adult|null",
          "skin_tone": "light|medium|dark|null", "face_visible": "bool", "framing": "head_and_shoulders|upper_body|full_body|distant|null"},
          "occupation_cues": "list of short strings (uniform, setting, equipment) or []", "setting": "short string", "photo_style": "colour|black_and_white|sepia|other"}
PROMPT = ("You are coding images for a research study of how image-generation loops treat people. Describe only what is visible. "
          "Return one JSON object and nothing else (no prose, no code fence), with exactly these keys: " + json.dumps(SCHEMA) +
          ". `primary` is the most prominent person (largest or most central); if no person is visible set person_present false, n_people 0 and every "
          "`primary` field null. gender_presentation is the apparent presentation, age_band the apparent age, skin_tone the apparent tone of the face "
          "in three bands (light, medium, dark). Use null whenever the face is too small, hidden or too stylised to tell.")


def parse_range(s, avail):
    if not s: return avail
    out = []
    for part in s.split(","):
        a, _, b = part.partition("-"); out.extend(range(int(a), int(b or a) + 1))
    return [x for x in out if x in set(avail)]


class Judge:
    def __init__(self, model=JUDGE_MODEL, retries=8):
        import anthropic
        _load_env()
        self.client = anthropic.Anthropic(max_retries=0, timeout=120); self.model = model; self.retries = retries
        self.anthropic = anthropic

    def judge(self, path):
        import anthropic
        b64 = base64.b64encode(pathlib.Path(path).read_bytes()).decode()
        last = None
        for attempt in range(self.retries):
            t0 = time.time()
            try:
                resp = self.client.messages.create(model=self.model, max_tokens=600, messages=[{"role": "user", "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": b64}}, {"type": "text", "text": PROMPT}]}])
                text = "".join(getattr(b, "text", "") for b in resp.content).strip()
                raw = text[text.find("{"): text.rfind("}") + 1]
                try:
                    parsed = json.loads(raw); err = None
                except Exception as e:  # noqa: BLE001
                    parsed, err = None, f"json: {e}"
                return {"judge": parsed, "judge_raw": text if parsed is None else None, "judge_error": err,
                        "judge_api": {"id": resp.id, "model": resp.model, "stop_reason": resp.stop_reason, "usage": {"input": resp.usage.input_tokens, "output": resp.usage.output_tokens}},
                        "judge_time_s": round(time.time() - t0, 2), "judge_attempts": attempt + 1, "temperature_applied": False}
            except (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
                last = e; time.sleep(min(60, 3 * 2 ** attempt))
            except anthropic.APIStatusError as e:
                if e.status_code == 529: last = e; time.sleep(min(60, 3 * 2 ** attempt))
                else: raise
        raise RuntimeError(f"judge failed after retries: {last!r}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("run"); ap.add_argument("--trajs"); ap.add_argument("--steps"); ap.add_argument("--parallel", type=int, default=8)
    ap.add_argument("--model", default=JUDGE_MODEL); ap.add_argument("--out"); ap.add_argument("--limit", type=int)
    a = ap.parse_args(argv)
    run_dir = ROOT / "runs" / a.run
    out = pathlib.Path(a.out) if a.out else CACHE / a.run / "judge.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        for line in out.read_text(encoding="utf-8").splitlines():
            if line.strip(): d = json.loads(line); done.add((d["traj"], d["step"]))
    avail = list_steps(run_dir)
    todo = [(t, s) for t in parse_range(a.trajs, sorted(avail)) for s in parse_range(a.steps, avail[t]) if (t, s) not in done]
    if a.limit: todo = todo[:a.limit]
    print(f"{a.run}: {len(done)} judged, {len(todo)} to do -> {out}")
    if not todo: return
    judge = Judge(a.model); t0 = time.time(); usage = [0, 0]
    with open(out, "a", encoding="utf-8") as f, ThreadPoolExecutor(max_workers=a.parallel) as ex:
        for i0 in range(0, len(todo), a.parallel):
            wave = todo[i0:i0 + a.parallel]
            for (t, s), rec in zip(wave, ex.map(lambda ts: judge.judge(image_path(run_dir, *ts)), wave)):
                f.write(json.dumps({"run": a.run, "traj": t, "step": s, **rec}) + "\n")
                usage[0] += rec["judge_api"]["usage"]["input"]; usage[1] += rec["judge_api"]["usage"]["output"]
            f.flush()
            n = i0 + len(wave)
            if n % 200 < a.parallel: print(f"  {n}/{len(todo)} {(time.time() - t0) / n:.2f} s/image, tokens in {usage[0]} out {usage[1]}", flush=True)
    print(f"done: {len(todo)} images in {(time.time() - t0) / 60:.1f} min; tokens in {usage[0]} out {usage[1]}")


if __name__ == "__main__":
    main()
