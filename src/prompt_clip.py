"""Clip a prompt to what SDXL's CLIP encoders would read (77 tokens: BOS + 75 content + EOS), SPEC2 §4 E1.

In A0 the cut happens inside SDXL. For generators with a wider text encoder (Hunyuan-DiT's mT5 reads 256 tokens) we
apply it explicitly, so every E1 cell gives its generator the same channel width as Hintze's loop. The clip keeps the
longest word prefix of the original text that fits, so the text itself is unchanged (CLIP's own token-level cut can end
mid-word and its decode lowercases). SDXL's tokenizer is the reference tokenizer.
"""
SDXL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
import re
CJK_RE = re.compile(r"[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef]")
SENT_PUNCT = "。！？；"      # back-off points for the character rule (sentence end first, then clause)
CLAUSE_PUNCT = "，、："


def cjk_share(text):
    t = "".join(text.split())
    return (len(CJK_RE.findall(t)) / len(t)) if t else 0.0


class PromptClipper:
    """tokenizer_id: HF repo whose `tokenizer/` subfolder is the reference (SDXL's CLIP by default; for E2 the generator's own
    repo, e.g. Hunyuan-DiT's bilingual CLIP, D15). revision pins the snapshot. For CJK text (no spaces, or CJK share >= 0.5)
    the cut is at character level, backed off to the last sentence/clause punctuation that keeps >= 60% of the fitting prefix."""

    def __init__(self, max_tokens=77, tokenizer_id=SDXL_ID, revision=None):
        from transformers import AutoTokenizer
        self.max_tokens = int(max_tokens)
        self.tokenizer_id = tokenizer_id; self.revision = revision
        kw = {"subfolder": "tokenizer"}
        if revision: kw["revision"] = revision
        self.tok = AutoTokenizer.from_pretrained(tokenizer_id, **kw)

    def count(self, text):
        return len(self.tok(text, truncation=False)["input_ids"])      # includes BOS and EOS

    def clip(self, text):
        """Returns (text_used, info). info: tokens_before, tokens_after, clipped, words_before, words_after."""
        n = self.count(text)
        words = text.split()
        cjk = len(words) <= 1 or cjk_share(text) >= 0.5
        units = list(text) if cjk else words
        join = (lambda u: "".join(u)) if cjk else (lambda u: " ".join(u))
        base = {"clip_tokens_before": n, "clip_max_tokens": self.max_tokens, "clip_rule": "char" if cjk else "word",
                "clip_words_before": len(words), "clip_chars_before": len(text)}
        if n <= self.max_tokens:
            return text, {**base, "clip_tokens_after": n, "clipped": False, "clip_words_after": len(words), "clip_chars_after": len(text)}
        # token count is monotone in the number of units kept, so binary-search the longest prefix that fits
        lo, hi = 0, len(units)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.count(join(units[:mid])) <= self.max_tokens:
                lo = mid
            else:
                hi = mid - 1
        if cjk and lo > 0:   # back off to the last sentence end, else clause end, that keeps >= 60% of the fitting prefix
            pref = join(units[:lo])
            for punct in (SENT_PUNCT, CLAUSE_PUNCT):
                cut = max((pref.rfind(ch) for ch in punct), default=-1)
                if cut + 1 >= 0.6 * lo:
                    lo = cut + 1; break
        used = join(units[:lo])
        return used, {**base, "clip_tokens_after": self.count(used), "clipped": True, "clip_words_after": len(used.split()), "clip_chars_after": len(used)}

    def info(self):
        return {"max_tokens": self.max_tokens, "tokenizer": self.tokenizer_id + "/tokenizer", "revision": self.revision,
                "rule": "longest word prefix (CJK text: longest character prefix, backed off to the last sentence/clause punctuation keeping >= 60%) with <= max_tokens tokens incl. BOS/EOS"}
