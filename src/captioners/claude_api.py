"""Claude captioner for A0-S (SPEC §5 / SPEC2 §4 E1 "second NEW captioner"): same interface as OllamaCaptioner.
Same request shape as Hintze's loop: the verbatim instruction plus the saved PNG, temperature T, nothing else (no system prompt,
no max_tokens below the instruction's own limit). API key from the environment or a git-ignored .env (CLAUDE.md); never logged.
Concurrency: the runner's captioner.parallel threads each call caption(); retries with backoff on 429 / 5xx / overloaded.
Every refusal and empty response is flagged in caption_flags and counted in the log."""
import base64, os, re, time
from pathlib import Path
from ..prompt_clip import CJK_RE
from .ollama_llava import REFUSAL_RE

ROOT = Path(__file__).resolve().parents[2]


def _load_env():
    if os.environ.get("ANTHROPIC_API_KEY"): return
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if line.startswith("ANTHROPIC_API_KEY=") and not line.startswith("#"):
                os.environ["ANTHROPIC_API_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")


class ClaudeCaptioner:
    def __init__(self, cfg: dict, temperature: float, logger=None):
        import anthropic
        _load_env()
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY not set (environment or .env); refusing to start the A0-S captioner")
        self.cfg = cfg; self.temperature = temperature; self.log = logger
        self.client = anthropic.Anthropic(max_retries=0, timeout=cfg.get("timeout_s", 120))
        self.model = cfg["model"]                     # pinned model id, e.g. claude-sonnet-5-5 (SPEC: pinned model ID)
        self.max_tokens = int(cfg.get("max_tokens", 400))
        self._info = None

    def info(self):
        if self._info is None:
            import anthropic
            self._info = {"backend": "anthropic", "model": self.model, "sdk_version": anthropic.__version__, "temperature": self.temperature,
                          "instruction": self.cfg["instruction"], "max_tokens": self.max_tokens, "system_prompt": None,
                          "request": "messages.create(model, max_tokens, temperature, messages=[{user: [image/png base64, text instruction]}])"}
        return dict(self._info)

    def caption(self, image_path, keep_alive=None):
        import anthropic
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
        last = None
        for attempt in range(self.cfg.get("retries", 8)):
            t0 = time.time()
            try:
                resp = self.client.messages.create(
                    model=self.model, max_tokens=self.max_tokens, temperature=self.temperature,
                    messages=[{"role": "user", "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
                        {"type": "text", "text": self.cfg["instruction"]}]}])
                text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
                words = len(text.split()); chars = len("".join(text.split())); cjk = len(CJK_RE.findall(text))
                meta = {"caption_time_s": round(time.time() - t0, 2),
                        "caption_api": {"id": resp.id, "model": resp.model, "stop_reason": resp.stop_reason,
                                        "input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens},
                        "caption_words": words, "caption_chars": chars, "caption_cjk_share": round((cjk / chars) if chars else 0.0, 3),
                        "caption_flags": {"empty": chars == 0, "over_50_words": words > 50, "refusal": bool(REFUSAL_RE.search(text)),
                                          "length_cutoff": resp.stop_reason == "max_tokens"},
                        "caption_attempts": attempt + 1}
                if (chars == 0 or meta["caption_flags"]["refusal"]) and self.log:
                    self.log.warning("%s caption for %s (attempt %d): %r", "empty" if chars == 0 else "refusal", image_path, attempt + 1, text[:120])
                return text, meta
            except (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
                last = e; wait = min(60, 2 ** attempt + 1)
                if self.log: self.log.warning("anthropic %s on %s; retry in %ds", type(e).__name__, image_path, wait)
                time.sleep(wait)
            except anthropic.APIStatusError as e:
                if e.status_code in (429, 529) or e.status_code >= 500:
                    last = e; wait = min(60, 2 ** attempt + 1)
                    if self.log: self.log.warning("anthropic status %s on %s; retry in %ds", e.status_code, image_path, wait)
                    time.sleep(wait)
                else:
                    raise
        raise RuntimeError(f"anthropic failed after retries: {last!r}")

    def unload(self):
        return None

    def loaded_models(self):
        return []
