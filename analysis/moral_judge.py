"""E3-P P4a (predictions.md "E3 second sample and projections", 2026-11-03): does each core-arm well instance one of the D menu's morals?
A Haiku judge reads one late story (steps 50-99) of e3_1_haiku_100 at a time and picks one of the five morals of the Haiku D cell's
anonymised menu (reports/e3_d.md) or "none of these". The judge sees no seed, step, well or model. Nothing it writes feeds any loop.

    .venv/bin/python analysis/moral_judge.py [--run e3_1_haiku_100] [--steps 50-99] [--parallel 4]      # judge, resumable
    .venv/bin/python analysis/moral_judge.py --report                                                     # per-well modal moral vs the sample

Output: analysis/cache/<run>/moral_judge.jsonl; report appended to reports/e3/projection.md and projection.json (key P4a).
"""
import argparse, collections, json, pathlib, sys, time
from concurrent.futures import ThreadPoolExecutor
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from common import ROOT, CACHE, cpu_only  # noqa: E402
from attribute_judge import _load_env, parse_range  # noqa: E402

MORALS = {1: "Grief is eased by small kindnesses from a community.",
          2: "Estranged siblings or relatives reconcile through shared grief; pride gives way to humility and honesty.",
          3: "Kindness ripples outward through strangers, each passing it on.",
          4: "A shared crisis dissolves old grudges between neighbours.",
          5: "Grief is softened through family rituals and shared memory."}
PROMPT = ("You are coding short stories for a research study. Below are five morals and a story. Pick the ONE moral that the story most clearly "
          "instances, or 0 if none of the five fits well. A moral fits only if it is what the story is about, not a passing element. Ignore all names. "
          "Return one JSON object and nothing else, like {\"moral\": 2}.\n\nMORALS:\n" + "\n".join(f"{k}. {v}" for k, v in MORALS.items()) + "\n0. None of these.")


class MoralJudge:
    def __init__(self, model="claude-haiku-5-5", retries=8):
        import anthropic; _load_env(); self.client = anthropic.Anthropic(max_retries=0, timeout=120); self.model = model; self.retries = retries

    def judge(self, story):
        import anthropic; last = None
        for attempt in range(self.retries):
            t0 = time.time()
            try:
                resp = self.client.messages.create(model=self.model, max_tokens=1500, output_config={"effort": "low"},
                                                   messages=[{"role": "user", "content": PROMPT + "\n\nSTORY:\n" + story}])
                text = "".join(getattr(b, "text", "") for b in resp.content if getattr(b, "type", "") == "text").strip()
                try: m = int(json.loads(text[text.find("{"): text.rfind("}") + 1])["moral"]); err = None if m in range(6) else "range"
                except Exception as e: m, err = None, f"parse: {e}"  # noqa: BLE001
                if err and attempt == 0: last = RuntimeError(err); continue
                return {"moral": m if not err else None, "raw": text if err else None, "error": err, "api": {"id": resp.id, "model": resp.model, "stop_reason": resp.stop_reason,
                        "usage": {"input": resp.usage.input_tokens, "output": resp.usage.output_tokens}}, "time_s": round(time.time() - t0, 2), "attempts": attempt + 1}
            except (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
                last = e; time.sleep(min(60, 3 * 2 ** attempt))
            except anthropic.APIStatusError as e:
                if e.status_code == 529: last = e; time.sleep(min(60, 3 * 2 ** attempt))
                else: raise
        raise RuntimeError(f"judge failed: {last!r}")


def run_judge(run, steps, parallel):
    out = CACHE / run / "moral_judge.jsonl"; out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        for line in out.read_text(encoding="utf-8").splitlines():
            if line.strip(): d = json.loads(line); done.add((d["traj"], d["step"]))
    todo = []
    for f in sorted((ROOT / "runs" / run).glob("traj_*/step_???.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        if r["step"] in steps and (r["traj"], r["step"]) not in done: todo.append((r["traj"], r["step"], r["story"]))
    print(f"{run}: {len(done)} judged, {len(todo)} to do -> {out}", flush=True)
    J = MoralJudge(); n = 0; t0 = time.time(); tin = tout = 0
    with ThreadPoolExecutor(parallel) as ex, open(out, "a", encoding="utf-8") as fh:
        for (t, s), res in zip([(a, b) for a, b, _ in todo], ex.map(lambda x: J.judge(x[2]), todo)):
            fh.write(json.dumps({"run": run, "traj": t, "step": s, **res}) + "\n"); fh.flush(); n += 1
            tin += res["api"]["usage"]["input"]; tout += res["api"]["usage"]["output"]
            if n % 200 == 0: print(f"  {n}/{len(todo)} {(time.time() - t0) / n:.2f} s/story", flush=True)
    print(f"done {n} in {(time.time() - t0) / 60:.1f} min; tokens in {tin} out {tout}; cost ${tin * 0.1e-6 + tout * 0.5e-6:.2f}", flush=True)


def report(run):
    from e3_projection import fit_reference, k_for, ATLAS, OUT
    from e3_report import unit
    from common import Cache
    from gravity import visits
    cpu_only(); X = unit(Cache(run).load("minilm_anon")["X"].astype(np.float64)[:, 1:]); steps = list(range(1, X.shape[1] + 1))
    C, L, pers, shared = fit_reference(X, k_for(X.shape[0] * X.shape[1]))
    J = {}
    for line in (CACHE / run / "moral_judge.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip(): d = json.loads(line); J[(d["traj"], d["step"])] = d["moral"]
    late = [m for (t, s), m in J.items() if m is not None]; overall = collections.Counter(late); n = len(late)
    rows = []; wells_ok = 0
    for c, ts, nv in shared:
        members = []
        for ti in ts:
            row = L[ti] == c; j = 0
            while j < len(row):                       # runs of consecutive inside-steps with their start index (visits() returns no start)
                if row[j]:
                    k0 = j
                    while j < len(row) and row[j]: j += 1
                    if j - k0 >= ATLAS["min_dwell"]:
                        for jj in range(k0, j):
                            m = J.get((ti, steps[jj]))
                            if m is not None: members.append(m)
                else: j += 1
        cnt = collections.Counter(members); modal, k = (cnt.most_common(1)[0] if cnt else (None, 0)); share = k / len(members) if members else None
        ok = modal not in (None, 0) and share >= 0.6; wells_ok += ok
        rows.append(dict(well=int(c), trajs=ts, member_stories_judged=len(members), modal_moral=modal, modal_share=share, counts=dict(cnt), ok=bool(ok)))
    none_share = overall[0] / n if n else None
    V = dict(wells=len(shared), wells_with_modal_moral_ge_060=wells_ok, none_share_all_late=none_share, overall={str(k): v / n for k, v in sorted(overall.items())},
             holds=wells_ok >= 9 and none_share is not None and none_share >= 0.4, rows=rows, n_judged=n)
    R = json.loads((OUT / "projection.json").read_text()); R.setdefault("verdicts", {})["P4a_judge"] = V; (OUT / "projection.json").write_text(json.dumps(R, indent=1, default=float))
    L_ = ["", "## P4a: core wells vs the D menu (Haiku judge, steps 50-99 of the reference sample)", "",
          f"{n} late stories judged; share picking none of the five morals {none_share:.2f}; overall shares " + ", ".join(f"{k}: {v:.2f}" for k, v in sorted(V['overall'].items())) + ".", "",
          "| well | trajectories | member stories judged | modal moral | share | counts |", "|---|---|---|---|---|---|"]
    for r in rows: L_.append(f"| {r['well']} | {r['trajs']} | {r['member_stories_judged']} | {r['modal_moral']} | {r['modal_share'] if r['modal_share'] is None else round(r['modal_share'], 2)} | {r['counts']} |")
    L_.append(f"\n**P4a**: {wells_ok} of {len(shared)} wells have a modal moral (not none) with >= 0.6 agreement (needs >= 9); none-share over all late stories {none_share:.2f} (needs >= 0.4): **{'holds' if V['holds'] else 'fails'}**.")
    with open(OUT / "projection.md", "a", encoding="utf-8") as fh: fh.write("\n".join(L_) + "\n")
    print("\n".join(L_))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--run", default="e3_1_haiku_100"); ap.add_argument("--steps", default="50-99"); ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--report", action="store_true"); a = ap.parse_args()
    if a.report: report(a.run)
    else: run_judge(a.run, set(parse_range(a.steps, list(range(100)))), a.parallel)


if __name__ == "__main__":
    main()
