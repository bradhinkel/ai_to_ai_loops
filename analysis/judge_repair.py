"""Salvage judge rows whose JSON did not parse on the first pass (analysis/attribute_judge.py leaves judge=null, judge_raw=text).
Two failure shapes were seen on E6: Sonnet writes a JSON object, then a prose "correction" and a second object (the second is
the one it means: last complete object wins); Haiku's reply is cut by max_tokens (unrecoverable, stays null).
Also normalises string booleans ("true"/"false") that Haiku sometimes emits for person_present / face_visible.
Rewrites the jsonl in place (backup <file>.orig), marks repaired rows with judge_repaired: "last_object" | "string_bool".

    .venv/bin/python analysis/judge_repair.py analysis/cache/e6_photo/judge.jsonl [...]
"""
import json, shutil, sys

def last_object(text):
    dec = json.JSONDecoder(); objs = []; i = 0
    while True:
        i = text.find("{", i)
        if i < 0: break
        try:
            o, end = dec.raw_decode(text, i); objs.append(o); i = end
        except json.JSONDecodeError:
            i += 1
    return objs[-1] if objs else None

def norm_bools(j):
    changed = False
    for d in (j, j.get("primary") or {}):
        for k in ("person_present", "face_visible"):
            if isinstance(d.get(k), str) and d[k].lower() in ("true", "false"):
                d[k] = d[k].lower() == "true"; changed = True
    return changed

for path in sys.argv[1:]:
    rows = [json.loads(l) for l in open(path) if l.strip()]
    n_last = n_bool = n_left = 0
    for x in rows:
        if x.get("judge_error") and x.get("judge_raw"):
            o = last_object(x["judge_raw"])
            if isinstance(o, dict) and "person_present" in o and "primary" in o:
                x["judge"] = o; x["judge_repaired"] = "last_object"; x["judge_error_original"] = x["judge_error"]; x["judge_error"] = None; n_last += 1
            else:
                n_left += 1
        if x.get("judge") and norm_bools(x["judge"]):
            x["judge_repaired"] = x.get("judge_repaired") or "string_bool"; n_bool += 1
    shutil.copy(path, path + ".orig")
    with open(path, "w") as f:
        for x in rows: f.write(json.dumps(x) + "\n")
    print(f"{path}: {len(rows)} rows; repaired last_object {n_last}, string_bool {n_bool}; still null {n_left}")
