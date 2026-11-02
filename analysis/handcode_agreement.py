"""Agreement between Brad's hand codes (reports/e3/handcode_sample.md, filled in place) and the Haiku judge's answers
(analysis/cache/e3_handcode_key.json): per-field percent agreement and Cohen's kappa over the stories Brad has filled.
Usage: .venv/bin/python analysis/handcode_agreement.py   (prints a table; writes reports/e3/handcode_agreement.md)"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
FIELDS = ["lead_age", "lead_gender", "lead_role_class", "setting_place", "setting_time", "conflict_type", "ending_valence",
          "secondary_character", "death_present", "reconciliation_present", "nature_central"]

def parse(md):
    out = {}
    for block in re.split(r"^## story ", md, flags=re.M)[1:]:
        sid = block.split("\n", 1)[0].strip()
        m = re.search(r"```\n(.*?)```", block, re.S)
        if not m: continue
        codes = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1); codes[k.strip()] = v.strip()
        if any(codes.get(f) for f in FIELDS): out[sid] = codes
    return out

def kappa(a, b):
    n = len(a); cats = set(a) | set(b)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan"), po

def main():
    hand = parse((ROOT / "reports/e3/handcode_sample.md").read_text(encoding="utf-8"))
    key = json.loads((ROOT / "analysis/cache/e3_handcode_key.json").read_text())
    rows = []; agree_all = []
    for f in FIELDS:
        a, b = [], []
        for sid, codes in hand.items():
            v = codes.get(f, "")
            if not v or sid not in key: continue
            j = key[sid]["judge"].get(f)
            a.append(str(v).lower()); b.append(str(j).lower())
        if a:
            k, po = kappa(a, b); rows.append((f, len(a), po, k)); agree_all.append(po)
    md = [f"# Hand-code agreement (Brad vs Haiku judge): {len(hand)} of {len(key)} stories filled", "",
          "| field | n | agreement | kappa |", "|---|---|---|---|"]
    md += [f"| {f} | {n} | {po:.2f} | {k:.2f} |" for f, n, po, k in rows]
    md += ["", f"Mean agreement over fields: {sum(agree_all)/len(agree_all):.2f}. B7's hand-code clause is reported when all 48 are filled; this is the running value."]
    # disagreements, for Brad
    md += ["", "## Disagreements", ""]
    for sid, codes in hand.items():
        if sid not in key: continue
        d = [(f, codes.get(f), key[sid]["judge"].get(f)) for f in FIELDS if codes.get(f) and str(codes.get(f)).lower() != str(key[sid]["judge"].get(f)).lower()]
        if d: md.append(f"- story {sid} ({key[sid]['run']} traj {key[sid]['traj']} step {key[sid]['step']}): " + "; ".join(f"{f}: Brad {b} / judge {j}" for f, b, j in d))
    (ROOT / "reports/e3/handcode_agreement.md").write_text("\n".join(md) + "\n", encoding="utf-8"); print("\n".join(md))

if __name__ == "__main__": main()
