"""Claude text generation for the E3 text loops: same interface as OllamaText. One user message (instruction + blank line + text),
no system prompt; the loop's T is probed once and, if the API rejects it (claude-sonnet-5-5, D16), the run proceeds at the model
default with temperature_applied=False in the manifest and every record. Thinking is left at the model's default (adaptive) with
output_config effort from the config (default low); thinking tokens are billed as output and recorded in usage. Refusals
(stop_reason "refusal") and empty responses are flagged and logged. Key from the environment or .env (CLAUDE.md); never logged."""
import os, time
from ..captioners.ollama_llava import REFUSAL_RE
from ..prompt_clip import CJK_RE
from ..captioners.claude_api import _load_env


def _cjk_share(text):
    chars = len("".join(text.split()))
    return round(len(CJK_RE.findall(text)) / chars, 3) if chars else 0.0


class ClaudeText:
    def __init__(self, cfg: dict, temperature: float, logger=None):
        import anthropic
        _load_env()
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY not set (environment or .env); refusing to start the Claude text backend")
        self.cfg = cfg; self.temperature = temperature; self.log = logger
        self.client = anthropic.Anthropic(max_retries=0, timeout=cfg.get("timeout_s", 180))
        self.model = cfg["model"]; self.effort = cfg.get("effort", "low")
        self.temperature_applied = True
        self._info = None
        self._probe_temperature()

    def _probe_temperature(self):
        import anthropic
        try:
            self.client.messages.create(model=self.model, max_tokens=1, messages=[{"role": "user", "content": "ok"}], extra_body={"temperature": self.temperature})
        except anthropic.BadRequestError as e:
            if "temperature" in str(e).lower():
                self.temperature_applied = False
                if self.log: self.log.warning("API rejects temperature=%s for %s: %s. Running at the model default (D16).", self.temperature, self.model, str(e)[:120])
            else:
                raise

    def info(self):
        import anthropic
        if self._info is None:
            self._info = {"backend": "anthropic", "model": self.model, "sdk_version": anthropic.__version__, "temperature": self.temperature,
                          "effort": self.effort, "thinking": "model default (adaptive)", "system_prompt": None,
                          "request": "messages.create(model, max_tokens, output_config={effort}, messages=[{user: instruction + blank line + text}], extra_body={temperature} if accepted)"}
        return dict(self._info, temperature_applied=self.temperature_applied)

    def _create(self, prompt, max_tokens):
        import anthropic
        kw = dict(model=self.model, max_tokens=max_tokens, output_config={"effort": self.effort}, messages=[{"role": "user", "content": prompt}])
        if self.temperature_applied:
            try:
                return self.client.messages.create(**kw, extra_body={"temperature": self.temperature})
            except anthropic.BadRequestError as e:
                if "temperature" not in str(e).lower(): raise
                self.temperature_applied = False
                if self.log: self.log.warning("API rejected temperature=%s (%s); continuing WITHOUT temperature control (D16).", self.temperature, str(e)[:160])
        return self.client.messages.create(**kw)

    def generate(self, prompt: str, keep_alive=None, max_tokens=None):
        import anthropic
        max_tokens = int(max_tokens or self.cfg.get("max_tokens", 4000))
        last = None
        for attempt in range(self.cfg.get("retries", 8)):
            t0 = time.time()
            try:
                resp = self._create(prompt, max_tokens)
                text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
                meta = {"time_s": round(time.time() - t0, 2),
                        "api": {"id": resp.id, "model": resp.model, "stop_reason": resp.stop_reason,
                                "input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens},
                        "chars": len("".join(text.split())), "cjk_share": _cjk_share(text),
                        "flags": {"empty": len(text) == 0, "refusal": resp.stop_reason == "refusal" or bool(REFUSAL_RE.search(text)),
                                  "length_cutoff": resp.stop_reason == "max_tokens", "cjk": _cjk_share(text) > 0.05},
                        "attempts": attempt + 1, "temperature_applied": self.temperature_applied}
                if (not text or meta["flags"]["refusal"]) and self.log:
                    self.log.warning("%s response (attempt %d, stop_reason %s): %r", "empty" if not text else "refusal", attempt + 1, resp.stop_reason, text[:120])
                return text, meta
            except (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
                last = e; wait = min(60, 2 ** attempt + 1)
                if self.log: self.log.warning("anthropic %s; retry in %ds", type(e).__name__, wait)
                time.sleep(wait)
            except anthropic.APIStatusError as e:
                if e.status_code in (429, 529) or e.status_code >= 500:
                    last = e; wait = min(60, 2 ** attempt + 1)
                    if self.log: self.log.warning("anthropic status %s; retry in %ds", e.status_code, wait)
                    time.sleep(wait)
                else:
                    raise
        raise RuntimeError(f"anthropic failed after retries: {last!r}")

    def unload(self):
        return None
