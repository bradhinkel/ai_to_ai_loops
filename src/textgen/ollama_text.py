"""Text-only generation via Ollama for the E3 text loops (SPEC2 §4 E3). Same request shape as the captioner minus the image:
the verbatim instruction, options={"temperature": T} and nothing else, response.strip() used as the next state without truncation.
The pinned digest is checked before the first call (D2 pattern)."""
import time
import ollama, requests
from ..captioners.ollama_llava import REFUSAL_RE
from ..prompt_clip import CJK_RE


def _cjk_share(text):
    chars = len("".join(text.split()))
    return round(len(CJK_RE.findall(text)) / chars, 3) if chars else 0.0


class OllamaText:
    def __init__(self, cfg: dict, temperature: float, logger=None):
        self.cfg = cfg; self.temperature = temperature; self.log = logger
        self.client = ollama.Client(host=cfg["host"], timeout=cfg.get("timeout_s", 600))
        self._info = None

    def info(self):
        if self._info is None:
            digest = None
            for m in self.client.list().models:
                if m.model == self.cfg["model"]:
                    digest = m.digest
            want = self.cfg.get("digest_prefix")
            if want and not (digest or "").startswith(want):
                raise RuntimeError(f"{self.cfg['model']} resolves to digest {digest!r}, not the pinned {want!r}; the tag moved. Do not run; report to Brad.")
            show = self.client.show(self.cfg["model"])
            try:
                version = requests.get(self.cfg["host"].rstrip("/") + "/api/version", timeout=10).json().get("version")
            except Exception:  # noqa: BLE001
                version = None
            self._info = {"backend": "ollama", "model": self.cfg["model"], "digest": digest, "ollama_version": version,
                          "details": dict(show.details) if show.details else None, "modelfile_parameters": show.parameters,
                          "temperature": self.temperature, "temperature_applied": True, "options_sent": {"temperature": self.temperature},
                          "request": "generate(model, prompt=instruction + blank line + text, options={temperature}, keep_alive)"}
        return dict(self._info)

    def generate(self, prompt: str, keep_alive=None, max_tokens=None):
        """Returns (text, meta). max_tokens is ignored on Ollama (no cap, as in the caption loop); done_reason records a cutoff."""
        last = None
        for attempt in range(self.cfg.get("retries", 5)):
            t0 = time.time()
            try:
                resp = self.client.generate(model=self.cfg["model"], prompt=prompt, options={"temperature": self.temperature}, keep_alive=keep_alive)
                text = (resp.response or "").strip()
                meta = {"time_s": round(time.time() - t0, 2),
                        "ollama": {k: getattr(resp, k, None) for k in ("done_reason", "total_duration", "load_duration", "prompt_eval_count", "prompt_eval_duration", "eval_count", "eval_duration")},
                        "chars": len("".join(text.split())), "cjk_share": _cjk_share(text),
                        "flags": {"empty": len(text) == 0, "refusal": bool(REFUSAL_RE.search(text)), "length_cutoff": getattr(resp, "done_reason", None) == "length",
                                  "cjk": _cjk_share(text) > 0.05},   # Qwen code-switches into Chinese (seen in the smoke); word counts undercount CJK text
                        "attempts": attempt + 1}
                if not text and self.log:
                    self.log.warning("empty response (attempt %d)", attempt + 1)
                return text, meta
            except Exception as e:  # noqa: BLE001
                last = e; wait = 5 * (attempt + 1)
                if self.log: self.log.warning("ollama error %r; retry in %ds", e, wait)
                time.sleep(wait)
        raise RuntimeError(f"ollama failed after retries: {last!r}")

    def unload(self):
        try:
            self.client.generate(model=self.cfg["model"], keep_alive=0)
        except Exception as e:  # noqa: BLE001
            if self.log: self.log.warning("unload request failed: %r", e)
