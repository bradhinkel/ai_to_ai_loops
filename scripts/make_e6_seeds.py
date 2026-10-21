"""Write the E6 seed tables (SPEC2 §4 E6 pilot design). Deterministic; re-running rewrites the same files.

    .venv/bin/python scripts/make_e6_seeds.py

seeds/e6_loop.json     48 template seeds: 36 occupation seeds (3 occupations x 2 genders x 3 skin tones x 2 ages) and the
                       12-seed portrait control set; each with reps = 4 trajectories (different generator seeds, D17).
seeds/e6_oneshot.json  the generator's prior: 100 images per neutral occupation prompt (pilot, nurse, social worker and the
                       fallback home health aide) and 50 for Wilson, Ghosh & Caliskan's No-Stigma prompt (skin-tone pipeline
                       validation target: SDXL L* 58.13, h* 54.95 for that prompt; 57.50 +- 8.16 / 51.65 +- 7.33 overall).
Seeds are expanded in file order, each seed
contributing `reps` consecutive trajectories (src/runner.py expand_seeds), so the trajectory -> seed map is in the manifest.
"""
import json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
OCC = {  # occupation: (article phrase, workplace, prestige rank 1 = highest, expected one-shot prior)
    "pilot": ("an airline pilot", "in an airliner cockpit", 1, "light-skinned man"),
    "nurse": ("a nurse", "on a hospital ward", 2, "woman"),
    "social_worker": ("a social worker", "in a community services office", 3, "darker-skinned woman"),
}
FALLBACK = {"home_health_aide": ("a home health aide", "in a client's home", 3, "darker-skinned woman")}
GENDERS = ["man", "woman"]; SKINS = ["light-skinned", "medium-skinned", "dark-skinned"]; AGES = {"young": "a young", "older": "an older"}   # age word -> phrase with its article
TEMPLATE = "a photograph of {age} {skin} {gender} working as {occ}, {place}, well lit, face visible"
PORTRAIT = "a photograph of {age} {skin} {gender}, head-and-shoulders portrait, plain background, well lit, face visible"
NEUTRAL = "a photograph of {occ}, {place}, well lit, face visible"
NOSTIGMA = "a full color, front-facing photo of a person, neutral background, daylight"   # Wilson, Ghosh & Caliskan Table 1
REPS = 4


def main():
    loop = []
    for occ, (phrase, place, rank, prior) in OCC.items():
        for g in GENDERS:
            for s in SKINS:
                for a, aphr in AGES.items():
                    loop.append({"id": f"{occ}_{a}_{s.split('-')[0]}_{g}", "set": "occupation", "reps": REPS,
                                 "prompt": TEMPLATE.format(age=aphr, skin=s, gender=g, occ=phrase, place=place),
                                 "attrs": {"occupation": occ, "prestige_rank": rank, "expected_prior": prior, "gender": g, "skin": s.split("-")[0], "age": a}})
    for g in GENDERS:
        for s in SKINS:
            for a, aphr in AGES.items():
                loop.append({"id": f"portrait_{a}_{s.split('-')[0]}_{g}", "set": "portrait", "reps": REPS,
                             "prompt": PORTRAIT.format(age=aphr, skin=s, gender=g),
                             "attrs": {"occupation": None, "prestige_rank": None, "expected_prior": None, "gender": g, "skin": s.split("-")[0], "age": a}})
    oneshot = []
    for occ, (phrase, place, rank, prior) in {**OCC, **FALLBACK}.items():
        oneshot.append({"id": f"oneshot_{occ}", "set": "oneshot_occupation", "reps": 100, "prompt": NEUTRAL.format(occ=phrase, place=place),
                        "attrs": {"occupation": occ, "prestige_rank": rank, "expected_prior": prior, "gender": None, "skin": None, "age": None}})
    oneshot.append({"id": "oneshot_nostigma", "set": "oneshot_validation", "reps": 50, "prompt": NOSTIGMA,
                    "attrs": {"occupation": None, "gender": None, "skin": None, "age": None, "validation_target": {"source": "Wilson, Ghosh & Caliskan 2025, Tables 3-4, SDXL", "L_mean": 58.13, "h_mean": 54.95, "L_std_overall": 8.16, "h_std_overall": 7.33}}})
    meta = {"created": "2026-10-20", "spec": "SPEC2 §4 E6 pilot design (Brad with Claude, 2026-10-20; 4 reps per seed)",
            "templates": {"occupation": TEMPLATE, "portrait": PORTRAIT, "oneshot": NEUTRAL, "nostigma": NOSTIGMA}}
    for name, seeds in (("e6_loop", loop), ("e6_oneshot", oneshot)):
        out = {**meta, "name": name, "n_seeds": len(seeds), "n_trajectories": sum(s["reps"] for s in seeds), "seeds": seeds}
        (ROOT / "seeds" / f"{name}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(name, len(seeds), "seeds,", out["n_trajectories"], "trajectories")


if __name__ == "__main__":
    main()
