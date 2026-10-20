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
        # anthropic SDK >= 1.x has no `temperature` argument on messages.create; the loop's T is sent as a raw body field and,
        # if the API rejects it, dropped once with temperature_applied=False recorded in info() and every record (deviation to log).
        self.temperature_applied = True
        self._info = None
        self._probe_temperature()

    def _probe_temperature(self):
        """One 1-token text call at start-up, so the manifest's captioner info records whether the API accepts the loop's T
        (claude-sonnet-5-5 rejects it, D16) before any caption is written."""
        import anthropic
        try:
            self.client.messages.create(model=self.model, max_tokens=1, messages=[{"role": "user", "content": "ok"}], extra_body={"temperature": self.temperature})
        except anthropic.BadRequestError as e:
            if "temperature" in str(e).lower():
                self.temperature_applied = False
                if self.log: self.log.warning("API rejects temperature=%s for %s: %s. Captions run at the model default (D16).", self.temperature, self.model, str(e)[:120])
            else:
                raise

    def info(self):
        if self._info is None:
            import anthropic
            self._info = {"backend": "anthropic", "model": self.model, "sdk_version": anthropic.__version__, "temperature": self.temperature,
                          "instruction": self.cfg["instruction"], "max_tokens": self.max_tokens, "system_prompt": None,
                          "request": "messages.create(model, max_tokens, messages=[{user: [image/png base64, text instruction]}], extra_body={temperature})"}
        return dict(self._info, temperature_applied=self.temperature_applied)

    def _create(self, img_b64):
        import anthropic
        kw = dict(model=self.model, max_tokens=self.max_tokens,
                  messages=[{"role": "user", "content": [
                      {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
                      {"type": "text", "text": self.cfg["instruction"]}]}])
        if self.temperature_applied:
            try:
                return self.client.messages.create(**kw, extra_body={"temperature": self.temperature})
            except anthropic.BadRequestError as e:
                if "temperature" not in str(e).lower(): raise
                self.temperature_applied = False
                if self.log: self.log.warning("API rejected temperature=%s for %s (%s); continuing WITHOUT temperature control. Record this in DEVIATIONS.md.", self.temperature, self.model, str(e)[:160])
        return self.client.messages.create(**kw)

    def caption(self, image_path, keep_alive=None):
        import anthropic
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
        last = None
        for attempt in range(self.cfg.get("retries", 8)):
            t0 = time.time()
            try:
                resp = self._create(img_b64)
                text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
                words = len(text.split()); chars = len("".join(text.split())); cjk = len(CJK_RE.findall(text))
                meta = {"caption_time_s": round(time.time() - t0, 2),
                        "caption_api": {"id": resp.id, "model": resp.model, "stop_reason": resp.stop_reason,
                                        "input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens},
                        "caption_words": words, "caption_chars": chars, "caption_cjk_share": round((cjk / chars) if chars else 0.0, 3),
                        "caption_flags": {"empty": chars == 0, "over_50_words": words > 50, "refusal": bool(REFUSAL_RE.search(text)),
                                          "length_cutoff": resp.stop_reason == "max_tokens"},
                        "caption_attempts": attempt + 1, "temperature_applied": self.temperature_applied}
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
