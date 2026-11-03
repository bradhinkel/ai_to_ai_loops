"""E3-E essay coding (predictions.md "E3-E essay-loop pilot", 2026-11-03, E3). A judge outside the loop reads one essay at a time, with no
knowledge of the seed, the step or the model, and fills a fixed schema: domain, subject kind (concrete vs abstract), stance, and a
one-sentence topic with no proper nouns. Schema fixed 2026-11-03 after reading the smoke essays (e3_e_haiku_smoke) and before any count.
Same client, retry and output conventions as theme_judge.py. Default judge claude-haiku-5-5.

    .venv/bin/python analysis/essay_judge.py e3_e_haiku [--steps 0-99] [--parallel 8]
Output: analysis/cache/<run>/essay_judge.jsonl, one line per (traj, step), incremental and resumable.
"""
import argparse, json, pathlib, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, CACHE  # noqa: E402
from attribute_judge import _load_env, parse_range  # noqa: E402

JUDGE_MODEL = "claude-haiku-5-5"
FIELDS = {
    "domain": ["science_and_nature", "technology", "history", "society_and_politics", "arts_and_culture", "philosophy_and_religion", "health_and_body", "economics", "mathematics", "places", "other"],
    "subject_kind": ["concrete", "abstract"],
    "stance": ["descriptive", "argues_a_position", "reflective_or_personal"],
    "time_frame": ["past", "present", "future", "timeless_or_mixed"],
    "mentions_ai_or_computing": ["yes", "no"],
    "mentions_environment_or_climate": ["yes", "no"],
    "tone": ["neutral", "hopeful", "cautionary", "critical", "celebratory"],
}
SCHEMA = {**{k: "|".join(v) for k, v in FIELDS.items()}, "topic": "one sentence of at most 20 words saying what the essay is about; no proper nouns",
          "position": "if stance is argues_a_position, the position in at most 15 words; otherwise 'none'"}
PROMPT = ("You are coding short essays for a research study of what essays produced by language-model text loops settle into. Code only what the "
          "text supports. Return one JSON object and nothing else (no prose, no code fence), with exactly these keys and allowed values: " + json.dumps(SCHEMA) +
          ". Definitions: domain is the field the essay mainly belongs to; subject_kind is concrete when the essay is about a specific thing, event, "
          "person, place, organism or technology, and abstract when it is about a theme, value, idea or question (e.g. connection, meaning, progress, "
          "responsibility); stance is descriptive when it explains or informs, argues_a_position when it advocates a view, reflective_or_personal when it "
          "muses or speaks in the first person; tone is the essay's overall emotional register. If the essay is not in English, code it anyway and write "
          "the topic in English.")


class Judge:
    def __init__(self, model=JUDGE_MODEL, retries=8, effort="low"):
        import anthropic; _load_env(); self.client = anthropic.Anthropic(max_retries=0, timeout=120); self.model = model; self.retries = retries; self.effort = effort

    def judge(self, text_in):
        import anthropic; last = None
        for attempt in range(self.retries):
            t0 = time.time()
            try:
                resp = self.client.messages.create(model=self.model, max_tokens=1500, output_config={"effort": self.effort},
                                                   messages=[{"role": "user", "content": PROMPT + "\n\nESSAY:\n" + text_in}])
                text = "".join(getattr(b, "text", "") for b in resp.content if getattr(b, "type", "") == "text").strip()
                raw = text[text.find("{"): text.rfind("}") + 1]
                try:
                    parsed = json.loads(raw); bad = [k for k, v in FIELDS.items() if parsed.get(k) not in v]; err = ("values: " + ",".join(bad)) if bad else None
                except Exception as e: parsed, err = None, f"json: {e}"  # noqa: BLE001
                if err and attempt == 0 and resp.stop_reason != "max_tokens": last = RuntimeError(err); continue
                return {"judge": parsed, "judge_raw": text if err else None, "judge_error": err,
                        "judge_api": {"id": resp.id, "model": resp.model, "stop_reason": resp.stop_reason, "usage": {"input": resp.usage.input_tokens, "output": resp.usage.output_tokens}},
                        "judge_time_s": round(time.time() - t0, 2), "judge_attempts": attempt + 1, "effort": self.effort, "temperature_applied": False}
            except (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
                last = e; time.sleep(min(60, 3 * 2 ** attempt))
            except anthropic.APIStatusError as e:
                if e.status_code == 529: last = e; time.sleep(min(60, 3 * 2 ** attempt))
                else: raise
        raise RuntimeError(f"judge failed after retries: {last!r}")


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("runs", nargs="+"); ap.add_argument("--steps"); ap.add_argument("--parallel", type=int, default=8); ap.add_argument("--model", default=JUDGE_MODEL)
    a = ap.parse_args(argv); J = Judge(a.model)
    for run in a.runs:
        out = CACHE / run / "essay_judge.jsonl"; out.parent.mkdir(parents=True, exist_ok=True); done = set()
        if out.exists():
            for line in out.read_text(encoding="utf-8").splitlines():
                if line.strip(): d = json.loads(line); done.add((d["traj"], d["step"]))
        todo = []
        for f in sorted((ROOT / "runs" / run).glob("traj_*/step_???.json")):
            r = json.loads(f.read_text(encoding="utf-8"))
            if r["step"] in set(parse_range(a.steps, list(range(1000)))) and (r["traj"], r["step"]) not in done: todo.append((r["traj"], r["step"], r["story"]))
        print(f"{run}: {len(done)} judged, {len(todo)} to do -> {out}", flush=True); t0 = time.time(); n = tin = tout = bad = 0
        with ThreadPoolExecutor(a.parallel) as ex, open(out, "a", encoding="utf-8") as fh:
            for (t, s, _), res in zip(todo, ex.map(lambda x: J.judge(x[2]), todo)):
                fh.write(json.dumps({"run": run, "traj": t, "step": s, **res}) + "\n"); fh.flush(); n += 1; bad += bool(res["judge_error"])
                tin += res["judge_api"]["usage"]["input"]; tout += res["judge_api"]["usage"]["output"]
                if n % 200 == 0: print(f"  {n}/{len(todo)} {(time.time() - t0) / n:.2f} s/essay, malformed {bad}", flush=True)
        print(f"{run} done: {n} essays in {(time.time() - t0) / 60:.1f} min; tokens in {tin} out {tout}; malformed {bad}; cost ${tin * 0.1e-6 + tout * 0.5e-6:.2f}", flush=True)


if __name__ == "__main__":
    main()
