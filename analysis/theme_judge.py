"""E3-B theme coding (SPEC2 §4 E3 follow-ups; predictions.md "E3 follow-ups" B1–B7). A judge outside the loop reads one story at a
time, with no knowledge of the seed, the step or the model that wrote it, and fills a fixed schema (categorical fields) plus a
one-sentence theme with no names of people or places. The judge is never the loop model's grading signal: nothing it writes is
fed back into any loop (CLAUDE.md rule 4 in spirit). Default judge claude-haiku-5-5; the second judge for reliability is
claude-sonnet-5-5 on a stratified subsample (--model, --out).

    .venv/bin/python analysis/theme_judge.py e3_1_sonnet e3_2_sonnet ... [--steps 0-99] [--parallel 8] [--model claude-haiku-5-5] [--limit N]
    .venv/bin/python analysis/theme_judge.py --sample 300 --model claude-sonnet-5-5 --suffix sonnet e3_1_sonnet ...   # reliability subsample

Output: analysis/cache/<run>/theme_judge[_<suffix>].jsonl, one line per (traj, step), incremental and resumable. Each line
carries the parsed JSON, the model id, request id and token usage. Sampling: the API gives no temperature control for these
models (D16); every call records that. CJK (Chinese) stories are sent as they are; the judge answers in the same schema.
"""
import argparse, json, pathlib, sys, time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import ROOT, CACHE, list_steps, read_record  # noqa: E402
from attribute_judge import _load_env, parse_range  # noqa: E402

JUDGE_MODEL = "claude-haiku-5-5"
FIELDS = {
    "lead_age": ["child", "teen", "young_adult", "middle_aged", "older_adult", "unclear"],
    "lead_gender": ["woman", "man", "other_or_unclear"],
    "lead_role_class": ["worker_or_tradesperson", "professional", "artist_or_craftsperson", "caregiver_or_parent", "student_or_child", "retired", "leader_or_official", "outsider_or_wanderer", "other_or_unclear"],
    "setting_place": ["home_interior", "small_town_or_village", "city", "rural_or_farmland", "wilderness_or_mountain", "coast_or_sea", "institution", "road_or_journey", "other_or_unclear"],
    "setting_time": ["present_day", "historical", "future_or_speculative", "unclear"],
    "conflict_type": ["interpersonal", "internal", "external_physical", "social_or_community", "none_or_unclear"],
    "ending_valence": ["hopeful", "bittersweet", "tragic", "neutral_or_ambiguous"],
    "secondary_character": ["none", "child", "parent_or_grandparent", "partner_or_spouse", "sibling", "friend", "stranger", "authority_or_mentor", "animal", "other"],
}
BOOLS = ["death_present", "reconciliation_present", "nature_central"]
SCHEMA = {**{k: "|".join(v) for k, v in FIELDS.items()}, **{b: "true|false" for b in BOOLS},
          "lead_role": "short string: the lead character's occupation or social role (e.g. 'retired fisherman', 'nurse', 'student'); 'unclear' if none",
          "theme": "one sentence of at most 25 words saying what the story is about; no names of people or places"}
PROMPT = ("You are coding short stories for a research study of what stories language-model text loops settle into. Code only what the text "
          "supports. Ignore every proper name: describe roles and kinds of place, never names. Return one JSON object and nothing else (no prose, "
          "no code fence), with exactly these keys and allowed values: " + json.dumps(SCHEMA) +
          ". Definitions: the lead is the character the story follows most; lead_age is the lead's apparent life stage (older_adult = roughly 60 or more, "
          "middle_aged = roughly 40-59, young_adult = roughly 18-39); setting_place is where most of the story happens (institution = hospital, school, "
          "office, prison, church and the like); conflict_type is the main tension (interpersonal = between people such as family, estrangement, romance; "
          "internal = grief, guilt, identity, a decision; external_physical = survival, danger, weather, illness as a physical threat; "
          "social_or_community = a community, workplace or society-level problem); ending_valence is how the story leaves the lead (hopeful = better off "
          "or at peace; bittersweet = loss and consolation together; tragic = worse off; neutral_or_ambiguous otherwise); death_present = someone dies or "
          "has recently died in the story; reconciliation_present = an estrangement or conflict between people is mended; nature_central = the natural "
          "world is central to the story, not just scenery. If the story is not in English, code it anyway and write the theme in English.")


class Judge:
    def __init__(self, model=JUDGE_MODEL, retries=8, effort="low"):
        import anthropic
        _load_env()
        self.client = anthropic.Anthropic(max_retries=0, timeout=120); self.model = model; self.retries = retries; self.effort = effort

    def judge(self, story):
        import anthropic
        last = None
        for attempt in range(self.retries):
            t0 = time.time()
            try:
                resp = self.client.messages.create(model=self.model, max_tokens=1500, output_config={"effort": self.effort},
                                                   messages=[{"role": "user", "content": PROMPT + "\n\nSTORY:\n" + story}])
                text = "".join(getattr(b, "text", "") for b in resp.content if getattr(b, "type", "") == "text").strip()
                raw = text[text.find("{"): text.rfind("}") + 1]
                try:
                    parsed = json.loads(raw); err = None
                    for b in BOOLS:                                   # the judge may spell booleans as strings; normalise
                        if isinstance(parsed.get(b), str) and parsed[b].strip().lower() in ("true", "false"): parsed[b] = parsed[b].strip().lower() == "true"
                    bad = [k for k, v in FIELDS.items() if parsed.get(k) not in v] + [b for b in BOOLS if not isinstance(parsed.get(b), bool)]
                    if bad: err = "values: " + ",".join(bad)
                except Exception as e:  # noqa: BLE001
                    parsed, err = None, f"json: {e}"
                if err and attempt == 0 and resp.stop_reason != "max_tokens":
                    last = RuntimeError(err); continue            # one re-ask on a malformed answer, then record it as is
                return {"judge": parsed, "judge_raw": text if err else None, "judge_error": err,
                        "judge_api": {"id": resp.id, "model": resp.model, "stop_reason": resp.stop_reason, "usage": {"input": resp.usage.input_tokens, "output": resp.usage.output_tokens}},
                        "judge_time_s": round(time.time() - t0, 2), "judge_attempts": attempt + 1, "effort": self.effort, "temperature_applied": False}
            except (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
                last = e; time.sleep(min(60, 3 * 2 ** attempt))
            except anthropic.APIStatusError as e:
                if e.status_code == 529: last = e; time.sleep(min(60, 3 * 2 ** attempt))
                else: raise
        raise RuntimeError(f"judge failed after retries: {last!r}")


def stratified(avail, n, seed=0):
    """n (traj, step) pairs per run, stratified over the gate's step windows (equal share per window), fixed seed."""
    import numpy as np
    rng = np.random.default_rng(seed); windows = [(1, 10), (11, 25), (26, 50), (51, 75), (76, 89), (90, 99)]
    pairs = [(t, s) for t in avail for s in avail[t]]; out = []
    for lo, hi in windows:
        pool = [p for p in pairs if lo <= p[1] <= hi]; k = min(len(pool), round(n / len(windows)))
        out += [pool[i] for i in sorted(rng.choice(len(pool), size=k, replace=False))]
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+"); ap.add_argument("--trajs"); ap.add_argument("--steps"); ap.add_argument("--parallel", type=int, default=8)
    ap.add_argument("--model", default=JUDGE_MODEL); ap.add_argument("--effort", default="low"); ap.add_argument("--suffix", default=""); ap.add_argument("--limit", type=int)
    ap.add_argument("--sample", type=int, help="per run: judge only a stratified sample of this many stories (reliability subsample)")
    a = ap.parse_args(argv)
    judge = Judge(a.model, effort=a.effort); grand = [0, 0]
    for run in a.runs:
        run_dir = ROOT / "runs" / run
        out = CACHE / run / f"theme_judge{('_' + a.suffix) if a.suffix else ''}.jsonl"; out.parent.mkdir(parents=True, exist_ok=True)
        done = set()
        if out.exists():
            for line in out.read_text(encoding="utf-8").splitlines():
                if line.strip(): d = json.loads(line); done.add((d["traj"], d["step"]))
        avail = list_steps(run_dir)
        if a.sample: todo = [p for p in stratified(avail, a.sample) if p not in done]
        else: todo = [(t, s) for t in parse_range(a.trajs, sorted(avail)) for s in parse_range(a.steps, avail[t]) if (t, s) not in done]
        if a.limit: todo = todo[:a.limit]
        print(f"{run}: {len(done)} judged, {len(todo)} to do -> {out}", flush=True)
        if not todo: continue
        t0 = time.time(); usage = [0, 0]; errors = 0
        with open(out, "a", encoding="utf-8") as f, ThreadPoolExecutor(max_workers=a.parallel) as ex:
            for i0 in range(0, len(todo), a.parallel):
                wave = todo[i0:i0 + a.parallel]
                for (t, s), rec in zip(wave, ex.map(lambda ts: judge.judge(read_record(run_dir, *ts)["story"]), wave)):
                    f.write(json.dumps({"run": run, "traj": t, "step": s, **rec}) + "\n")
                    usage[0] += rec["judge_api"]["usage"]["input"]; usage[1] += rec["judge_api"]["usage"]["output"]; errors += bool(rec["judge_error"])
                f.flush()
                n = i0 + len(wave)
                if n % 400 < a.parallel: print(f"  {n}/{len(todo)} {(time.time() - t0) / n:.2f} s/story, tokens in {usage[0]} out {usage[1]}, malformed {errors}", flush=True)
        grand[0] += usage[0]; grand[1] += usage[1]
        print(f"{run} done: {len(todo)} stories in {(time.time() - t0) / 60:.1f} min; tokens in {usage[0]} out {usage[1]}; malformed {errors}", flush=True)
    print(f"all done; tokens in {grand[0]} out {grand[1]}")


if __name__ == "__main__":
    main()
