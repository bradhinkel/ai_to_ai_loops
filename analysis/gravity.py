"""Attractor 'gravity' (Brad, 2026-10-19): the loop is a stochastic process (SDXL noise, LLM sampling), so an attractor is a
metastable state, not an absorbing one. Its pull is two numbers, estimated from every intermediate step in DINOv2 space:

  depth  = per-step escape hazard h_k = exits / trajectory-steps spent inside k  (mean residence ~ 1/h_k; the final step is
           censored, so a Kaplan-Meier median residence is also given);
  pull   = capture rate c_k = entries into k / trajectory-steps spent outside k.

The single summary is the stationary share of the coarse-grained Markov chain over {attractors, free}, which is what the
endpoint histogram would converge to if the loop ran forever; it is compared with the observed step-99 share. Also reported:
hazard as a function of depth inside the basin (distance / radius) and as a function of step (a Markov loop should be flat).

States: archive centroids (--archive) or k-means on the run's own step-99 embeddings (k = knee unless --k). Membership uses
ONE fixed radius for every attractor (--radius, default 0.20 cosine) so that gravity is comparable across attractors and
runs; the archive's own p95 radii (0.11-0.79 for A0-core) would make loose k-means groups look like deep wells. Hysteresis:
once inside, a trajectory stays labelled until it is beyond --exit_factor x radius (default 1.25), suppressing boundary flicker.
CLIP is not used.

    .venv/bin/python analysis/gravity.py a0_core --archive archive/a0_core_centroids.npz
    .venv/bin/python analysis/gravity.py e1_cap_pilot
    .venv/bin/python analysis/gravity.py a0_core --archive archive/a0_core_centroids.npz --space minilm --radius 0.15   # caption space; same captioner => comparable across generators
Writes reports/gravity_<run>.md and .json.
"""
import argparse, json, pathlib, sys
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import Cache, cpu_only, kmeans, elbow_k, ROOT  # noqa: E402


def label_steps(D, R, exit_factor):
    """D [K,T,S] distances; returns labels [T,S] with -1 = free, using fixed radii R[k] and hysteresis."""
    near = D.argmin(0); dmin = D.min(0); lab = np.where(dmin <= R[near], near, -1)
    out = lab.copy()
    for t in range(lab.shape[0]):
        cur = -1
        for s in range(lab.shape[1]):
            if cur >= 0 and D[cur, t, s] <= exit_factor * R[cur]: out[t, s] = cur
            else: cur = lab[t, s]; out[t, s] = cur
    return out


def km_median(done, censored):
    """Kaplan-Meier median residence (steps) from completed dwell lengths and right-censored ones; None if S(t) never drops below 0.5."""
    times = sorted(set(done)); n = len(done) + len(censored); S = 1.0
    for t in times:
        at_risk = sum(1 for d in done if d >= t) + sum(1 for c in censored if c >= t)
        S *= 1 - done.count(t) / at_risk
        if S <= 0.5: return t
    return None


def visits(inside_row):
    runs, cur = [], 0
    for v in inside_row:
        if v: cur += 1
        elif cur: runs.append((cur, False)); cur = 0
    if cur: runs.append((cur, True))
    return runs


def main():
    cpu_only()
    ap = argparse.ArgumentParser()
    ap.add_argument("run"); ap.add_argument("--archive", default=None); ap.add_argument("--k", type=int, default=0)
    ap.add_argument("--radius", type=float, default=0.20); ap.add_argument("--exit_factor", type=float, default=1.25)
    ap.add_argument("--labels", default=None, help="optional json list of attractor names, index = probe")
    ap.add_argument("--space", default="dinov2", choices=["dinov2", "minilm"], help="embedding space for states and membership (archive must hold centroid_<space>)")
    a = ap.parse_args()
    B = Cache(a.run).arrays(a.space); X = B["X"].astype(np.float64); steps = list(B["steps"]); mask = B["mask"]; i99 = steps.index(99)
    if a.archive:
        z = np.load(a.archive, allow_pickle=True); C = z[f"centroid_{a.space}"].astype(np.float64); source = f"{a.archive} ({a.space})"
        sizes = [len(m) for m in z["members"]]
    else:
        ok = mask[:, i99]; E = X[ok, i99]; k = a.k or elbow_k(E)[0] or min(10, len(E) // 2); km = kmeans(E, k)
        C = np.stack([E[km.labels_ == c].mean(0) for c in range(k)]); source = f"k-means k={k} on {a.run} step-99 {a.space}"
        sizes = [int((km.labels_ == c).sum()) for c in range(k)]
    names = json.loads(pathlib.Path(a.labels).read_text()) if a.labels else [f"attractor {k}" for k in range(len(C))]
    C = C / np.linalg.norm(C, axis=1, keepdims=True); K = len(C); R = np.full(K, a.radius)
    D = 1 - np.einsum("pd,tsd->pts", C, X); D[:, ~mask] = np.inf
    L = label_steps(D, R, a.exit_factor); T, S = L.shape
    rows = []
    for k in range(K):
        inside = L == k; s_in = inside[:, :-1]; n_in = inside[:, 1:]
        exits = int((s_in & ~n_in).sum()); stay = int(s_in.sum()); entries = int((~s_in & n_in).sum()); out = int((~s_in).sum())
        h = exits / stay if stay else None; c = entries / out if out else None
        done, cens, reent = [], [], 0
        for t in range(T):
            v = visits(inside[t]); reent += max(len(v) - 1, 0)
            for n, cen in v: (cens if cen else done).append(n)
        rows.append(dict(k=k, name=names[k], size_at_definition=sizes[k], endpoints=int(inside[:, i99].sum()), steps_inside=stay, entries=entries, exits=exits,
                         hazard=h, mean_residence=(1 / h if h else None), km_median_residence=km_median(done, cens) if (done or cens) else None,
                         capture=c, reentries=reent, n_visits_completed=len(done), n_visits_censored=len(cens),
                         max_completed_dwell=max(done) if done else 0))
    # coarse chain
    M = np.zeros((K + 1, K + 1))
    for t in range(T):
        for s in range(S - 1): M[L[t, s], L[t, s + 1]] += 1
    Ms = M.copy(); Ms[:K, K] += 0.5; Ms[K, :K] += 0.5   # Jeffreys pseudo-counts: a state with no observed exit is not absorbing
    P = Ms / np.maximum(Ms.sum(1, keepdims=True), 1)
    w, v = np.linalg.eig(P.T); pi = np.real(v[:, np.argmax(np.real(w))]); pi = np.clip(pi / pi.sum(), 0, None); pi /= pi.sum()
    end_share = np.bincount(L[:, i99] % (K + 1), minlength=K + 1) / T
    for k in range(K): rows[k]["stationary_share"] = float(pi[k]); rows[k]["endpoint_share"] = float(end_share[k])
    # hazard by depth and by step (pooled)
    depth = np.full(L.shape, np.nan)
    for k in range(K):
        m = L == k; depth[m] = D[k][m] / R[k]
    bins = [0, .4, .6, .8, 1.0, a.exit_factor]; by_depth = []
    for lo, hi in zip(bins[:-1], bins[1:]):
        m = (depth[:, :-1] >= lo) & (depth[:, :-1] < hi); n = int(m.sum())
        by_depth.append(dict(lo=lo, hi=hi, n=n, exit_rate=float((L[:, :-1][m] != L[:, 1:][m]).mean()) if n else None))
    by_step = []
    for a0, a1 in [(0, 20), (20, 40), (40, 60), (60, 80), (80, S - 1)]:
        ins = L[:, a0:a1] >= 0; n = int(ins.sum())
        by_step.append(dict(lo=a0, hi=a1, n=n, exit_rate=float((L[:, a0:a1][ins] != L[:, a0 + 1:a1 + 1][ins]).mean()) if n else None))
    f = lambda x, p=3: "-" if x is None else (f"{x:.{p}f}" if isinstance(x, float) else str(x))
    lines = [f"# Attractor gravity: {a.run} ({a.space})", "",
             f"States: {source}. Fixed radius {a.radius} ({a.space} cosine), exit at {a.exit_factor}x radius (hysteresis). {T} trajectories x {S} steps; "
             f"free share of all steps {np.mean(L == -1):.2f}. hazard = exits / steps inside (per step); capture = entries / steps outside (per step); "
             f"KM median = Kaplan-Meier median residence (final step censored); stationary = long-run share of the coarse chain over attractors + free (0.5 pseudo-count on every attractor<->free transition, so a state with no observed exit is not treated as absorbing).", "",
             "| k | attractor | endpoints | steps inside | entries | exits | hazard /step | mean residence | KM median | capture /step | re-entries | longest completed visit | stationary share | endpoint share |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: -r["stationary_share"]):
        lines.append(f"| {r['k']} | {r['name']} | {r['endpoints']} | {r['steps_inside']} | {r['entries']} | {r['exits']} | {f(r['hazard'])} | {f(r['mean_residence'], 1)} | {f(r['km_median_residence'])} | "
                     f"{f(r['capture'], 4)} | {r['reentries']} | {r['max_completed_dwell']} | {r['stationary_share']:.3f} | {r['endpoint_share']:.2f} |")
    lines += [f"| - | free | {int(end_share[K] * T)} | | | | | | | | | | {pi[K]:.3f} | {end_share[K]:.2f} |", "",
              "Exit rate by depth inside the basin (distance / radius, pooled over attractors):", "", "| d/R | n steps | exit rate |", "|---|---|---|"]
    lines += [f"| [{b['lo']:.2f}, {b['hi']:.2f}) | {b['n']} | {f(b['exit_rate'])} |" for b in by_depth]
    lines += ["", "Exit rate by step window (pooled; a stationary loop is flat):", "", "| steps | n inside | exit rate |", "|---|---|---|"]
    lines += [f"| {b['lo']}-{b['hi']} | {b['n']} | {f(b['exit_rate'])} |" for b in by_step]
    md = "\n".join(lines) + "\n"; sfx = "" if a.space == "dinov2" else f"_{a.space}"
    (ROOT / "reports" / f"gravity_{a.run}{sfx}.md").write_text(md)
    (ROOT / "reports" / f"gravity_{a.run}{sfx}.json").write_text(json.dumps(dict(run=a.run, source=source, radius=a.radius, exit_factor=a.exit_factor,
                                                                            attractors=rows, free_stationary=float(pi[K]), free_endpoint=float(end_share[K]),
                                                                            hazard_by_depth=by_depth, hazard_by_step=by_step, transition_counts=M.tolist()), indent=1))
    print(md)


if __name__ == "__main__":
    main()
