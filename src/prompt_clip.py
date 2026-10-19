"""Clip a prompt to what SDXL's CLIP encoders would read (77 tokens: BOS + 75 content + EOS), SPEC2 §4 E1.

In A0 the cut happens inside SDXL. For generators with a wider text encoder (Hunyuan-DiT's mT5 reads 256 tokens) we
apply it explicitly, so every E1 cell gives its generator the same channel width as Hintze's loop. The clip keeps the
longest word prefix of the original text that fits, so the text itself is unchanged (CLIP's own token-level cut can end
mid-word and its decode lowercases). SDXL's tokenizer is the reference tokenizer.
"""
SDXL_ID = "stabilityai/stable-diffusion-xl-base-1.0"


class PromptClipper:
    def __init__(self, max_tokens=77, tokenizer_id=SDXL_ID):
        from transformers import CLIPTokenizer
        self.max_tokens = int(max_tokens)
        self.tokenizer_id = tokenizer_id
        self.tok = CLIPTokenizer.from_pretrained(tokenizer_id, subfolder="tokenizer")

    def count(self, text):
        return len(self.tok(text, truncation=False)["input_ids"])      # includes BOS and EOS

    def clip(self, text):
        """Returns (text_used, info). info: tokens_before, tokens_after, clipped, words_before, words_after."""
        n = self.count(text)
        words = text.split()
        if n <= self.max_tokens:
            return text, {"clip_tokens_before": n, "clip_tokens_after": n, "clipped": False,
                          "clip_words_before": len(words), "clip_words_after": len(words), "clip_max_tokens": self.max_tokens}
        # token count is monotone in the number of words kept, so binary-search the longest prefix that fits
        lo, hi = 0, len(words)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.count(" ".join(words[:mid])) <= self.max_tokens:
                lo = mid
            else:
                hi = mid - 1
        used = " ".join(words[:lo])
        return used, {"clip_tokens_before": n, "clip_tokens_after": self.count(used), "clipped": True,
                      "clip_words_before": len(words), "clip_words_after": lo, "clip_max_tokens": self.max_tokens}

    def info(self):
        return {"max_tokens": self.max_tokens, "tokenizer": self.tokenizer_id + "/tokenizer", "rule": "longest word prefix with <= max_tokens CLIP tokens incl. BOS/EOS"}
