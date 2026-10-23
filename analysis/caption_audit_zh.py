"""Caption audit for Chinese-instruction cells (E2-QZ, D15) with the English control alongside. From the step records only.

  analysis/caption_audit_zh.py e2_qz e1_both   -> reports/caption_audit_e2_qz.md + .json

Per run and step window: characters (CJK rule) or words, CJK share, share of captions in Chinese (CJK share >= 0.5), clip
rate (CLIP-77, character rule for CJK), over-limit flag, people / gendered terms, style vocabulary, and East Asian motif
vocabulary. Chinese and English term lists are fixed here so both runs are counted the same way; substring matching for
Chinese (no word boundaries), word matching for English. A Chinese caption is scored with the Chinese lists, an English
caption with the English lists (per-caption language by CJK share).
"""
import argparse, json, re, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent)); from common import ROOT, caption_used  # noqa: E402
sys.path.insert(0, str(ROOT)); from src.prompt_clip import cjk_share  # noqa: E402

# ---- Chinese lists (substring). Exclusions stop common non-person compounds of 人 and the neutral 他们.
PEOPLE_ZH = ["人", "身影", "女", "男", "孩", "她", "他", "舞者", "行人", "旅人", "情侣", "家人", "老人", "母亲", "父亲", "僧", "武士",
             "仙女", "女神", "新娘", "少年", "青年", "骑士", "战士", "王子", "公主", "一家", "渔夫", "农夫", "牧人", "修行者", "僧侣"]
PEOPLE_ZH_EXCL = ["无人", "人造", "人间", "迷人", "动人", "惊人", "人工", "诱人", "宜人", "人心", "引人", "撩人", "醉人", "他们"]
MALE_ZH = ["男", "他", "父亲", "王子", "国王", "武士", "骑士", "僧", "先生", "老翁", "渔夫", "农夫", "牧人"]
MALE_ZH_EXCL = ["他们", "其他"]
FEMALE_ZH = ["女", "她", "母亲", "公主", "新娘", "女王"]
STYLE_ZH = ["梦幻", "艺术", "诗意", "壮丽", "宁静", "绚丽", "绚烂", "璀璨", "唯美", "神秘", "空灵", "如画", "水彩", "油画", "画卷", "笔触",
            "光影", "斑斓", "梦境", "仙境", "静谧", "缥缈", "朦胧", "浪漫", "金辉", "光芒", "辉煌", "奇幻", "幻境", "绮丽", "瑰丽"]
EAST_ASIAN_ZH = {
    "architecture": ["宝塔", "凉亭", "亭", "庭院", "园林", "寺", "古建筑", "飞檐", "屋檐", "牌坊", "古镇", "石桥", "拱桥", "长城", "中式", "东方", "日式", "宫灯", "殿宇", "阁楼", "楼阁"],
    "nature": ["富士", "樱花", "樱", "竹", "梅花", "荷花", "莲花", "莲", "锦鲤", "鹤", "龙", "松柏", "桃花"],
    "dress_art": ["汉服", "旗袍", "和服", "水墨", "书法", "古风", "折扇", "油纸伞", "灯笼", "禅", "武士", "僧", "笛", "古筝", "琵琶"],
}
# ---- English lists (words / phrases), same categories
PEOPLE_EN = {"person", "people", "man", "woman", "men", "women", "boy", "girl", "child", "children", "figure", "figures", "couple", "crowd",
             "family", "lady", "gentleman", "individual", "individuals", "silhouette", "silhouettes", "he", "she", "his", "her", "they",
             "someone", "player", "players", "dancer", "dancers", "hiker", "hikers", "traveler", "travelers", "travellers", "monk", "monks"}
MALE_EN = {"man", "men", "boy", "boys", "he", "his", "him", "gentleman", "gentlemen", "male", "father", "king", "prince"}
FEMALE_EN = {"woman", "women", "girl", "girls", "she", "her", "hers", "lady", "ladies", "female", "mother", "queen", "princess"}
STYLE_EN = {"vibrant", "vivid", "ethereal", "dreamlike", "dreamy", "surreal", "whimsical", "painterly", "painted", "painting", "brushstrokes",
            "watercolor", "impressionist", "luminous", "glowing", "radiant", "enchanting", "enchanted", "magical", "mystical", "otherworldly",
            "fantastical", "kaleidoscopic", "iridescent", "shimmering", "swirling", "swirls", "artistic", "stylized", "abstract", "majestic",
            "breathtaking", "celestial", "mesmerizing", "opulent", "ornate", "gilded", "golden", "hues", "palette", "canvas", "serene", "tranquil"}
EAST_ASIAN_EN = {
    "architecture": ["pagoda", "pagodas", "temple", "temples", "shrine", "torii", "oriental", "chinese", "japanese", "asian", "zen garden", "tiled roof", "curved roof"],
    "nature": ["fuji", "cherry blossom", "cherry blossoms", "sakura", "bamboo", "koi", "lotus flower", "lotus flowers", "lotus pond", "dragon", "plum blossom"],
    "dress_art": ["kimono", "hanfu", "qipao", "cheongsam", "geisha", "samurai", "ink wash", "ink-wash", "calligraphy", "lantern", "lanterns", "zen", "monk", "monks", "bonsai"],
}
WINDOWS = [(0, 0), (1, 5), (6, 10), (11, 25), (26, 50), (51, 75), (76, 99)]


def count_zh(text, terms, excl=()):
    t = text
    for e in excl: t = t.replace(e, "□" * len(e))
    return sum(t.count(x) for x in terms)


def words_en(text): return re.findall(r"[a-z][a-z'\-]*", text.lower())


def score(cap):
    zh = cjk_share(cap) >= 0.5
    if zh:
        people = count_zh(cap, PEOPLE_ZH, PEOPLE_ZH_EXCL) > 0
        male = count_zh(cap, MALE_ZH, MALE_ZH_EXCL); female = count_zh(cap, FEMALE_ZH)
        style = count_zh(cap, STYLE_ZH) > 0
        ea = {c: count_zh(cap, v) > 0 for c, v in EAST_ASIAN_ZH.items()}
        length = len(cap.strip())
    else:
        w = words_en(cap); ws = set(w); lw = cap.lower()
        people = bool(ws & PEOPLE_EN); male = sum(1 for x in w if x in MALE_EN); female = sum(1 for x in w if x in FEMALE_EN)
        style = bool(ws & STYLE_EN)
        ea = {c: any((p in ws) if " " not in p and "-" not in p else (p in lw) for p in v) for c, v in EAST_ASIAN_EN.items()}
        length = len(w)
    return dict(zh=zh, length=length, cjk=cjk_share(cap), people=people, male=male, female=female, style=style,
                ea_any=any(ea.values()), **{f"ea_{c}": v for c, v in ea.items()})


def audit(run):
    run_dir = ROOT / "runs" / run; rows = []
    for f in sorted(run_dir.glob("traj_*/step_*.json")):
        if f.name.endswith(".gen.json"): continue
        r = json.load(open(f, encoding="utf-8"))
        cap = caption_used(run_dir, int(r["traj"]), int(r["step"]), r) or ""
        fl = r.get("caption_flags", {})
        rows.append(dict(step=r["step"], traj=r["traj"], clipped=bool(r.get("clipped", False)), clip_rule=r.get("clip_rule"),
                         over_limit=bool(fl.get("over_limit_chars") or fl.get("over_50_words")), not_cjk=bool(fl.get("not_cjk")),
                         empty=bool(fl.get("empty")), refusal=bool(fl.get("refusal")), cutoff=bool(fl.get("length_cutoff")),
                         mt5_trunc=bool(r.get("prompt_truncated_by_mt5", False)), **score(cap)))
    out = {"run": run, "n_records": len(rows), "windows": []}
    for lo, hi in WINDOWS:
        sub = [x for x in rows if lo <= x["step"] <= hi]
        if not sub: continue
        n = len(sub); sh = lambda k: float(np.mean([bool(x[k]) for x in sub]))  # noqa: E731
        out["windows"].append(dict(steps=f"{lo}-{hi}" if lo != hi else str(lo), n=n,
                                   length_median=float(np.median([x["length"] for x in sub])),
                                   length_p90=float(np.percentile([x["length"] for x in sub], 90)),
                                   zh_share=sh("zh"), cjk_median=float(np.median([x["cjk"] for x in sub])),
                                   clipped=sh("clipped"), over_limit=sh("over_limit"), not_cjk_flag=sh("not_cjk"), empty=sh("empty"),
                                   refusal=sh("refusal"), cutoff=sh("cutoff"), mt5_trunc=sh("mt5_trunc"),
                                   people=sh("people"), male=int(sum(x["male"] for x in sub)), female=int(sum(x["female"] for x in sub)),
                                   style=sh("style"), ea_any=sh("ea_any"), ea_architecture=sh("ea_architecture"), ea_nature=sh("ea_nature"),
                                   ea_dress_art=sh("ea_dress_art")))
    # per-step series for the figure / report
    out["ea_any_by_step"] = [float(np.mean([x["ea_any"] for x in rows if x["step"] == s])) for s in range(100)]
    out["people_by_step"] = [float(np.mean([x["people"] for x in rows if x["step"] == s])) for s in range(100)]
    out["ea_any_trajs_step99"] = int(sum(1 for x in rows if x["step"] == 99 and x["ea_any"]))
    out["ea_any_trajs_any_step_ge50"] = len({x["traj"] for x in rows if x["step"] >= 50 and x["ea_any"]})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("runs", nargs="+"); ap.add_argument("--out", default="reports/caption_audit_e2_qz")
    a = ap.parse_args(argv); res = [audit(r) for r in a.runs]
    md = ["# Caption audit (Chinese-aware): " + ", ".join(a.runs) + "\n",
          "Length = characters for Chinese captions (CJK share >= 0.5), words for English. Chinese term lists are substrings (people excludes 无人/迷人/动人/他们 etc.); "
          "English lists are words. East Asian motif vocabulary: architecture (pagoda, pavilion, temple, courtyard garden, curved eaves, ...), nature (Fuji, cherry "
          "blossom, bamboo, lotus, koi, crane, dragon), dress/art (hanfu, qipao, kimono, ink wash, calligraphy, lantern, zen, monk). "
          "Male/female = total gendered-term counts in the window. Clip = CLIP-77 clip fired (character rule for CJK).\n"]
    for r in res:
        md.append(f"## {r['run']} ({r['n_records']} records)\n")
        md.append("| steps | n | length median / p90 | in Chinese | clip | over limit | empty / refusal / cutoff | people | male : female | style | EA any | EA arch | EA nature | EA dress/art |")
        md.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for w in r["windows"]:
            md.append(f"| {w['steps']} | {w['n']} | {w['length_median']:.0f} / {w['length_p90']:.0f} | {w['zh_share']:.3f} | {w['clipped']:.3f} | {w['over_limit']:.3f} | "
                      f"{w['empty']:.3f} / {w['refusal']:.3f} / {w['cutoff']:.3f} | {w['people']:.2f} | {w['male']} : {w['female']} | {w['style']:.2f} | "
                      f"{w['ea_any']:.3f} | {w['ea_architecture']:.3f} | {w['ea_nature']:.3f} | {w['ea_dress_art']:.3f} |")
        md.append(f"\nTrajectories whose step-99 caption carries an East Asian motif term: {r['ea_any_trajs_step99']} / 100; with one anywhere in steps 50-99: {r['ea_any_trajs_any_step_ge50']}.\n")
    Path(a.out + ".md").write_text("\n".join(md), encoding="utf-8"); json.dump(res, open(a.out + ".json", "w"), indent=1, ensure_ascii=False)
    print("\n".join(md))


if __name__ == "__main__":
    main()
