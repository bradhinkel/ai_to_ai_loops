"""LLaVA via Ollama, matching OSFcontinue.describe_image(): the verbatim instruction, the saved PNG base64-encoded,
options={"temperature": T} and nothing else, response.strip() used as the next prompt without truncation."""
import base64, re, time
from ..prompt_clip import CJK_RE
import ollama, requests

REFUSAL_RE = re.compile(r"\b(I'm sorry|I cannot|I can't|as an AI|unable to (?:describe|assist))\b", re.I)


class OllamaCaptioner:
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
                          "temperature": self.temperature, "instruction": self.cfg["instruction"], "options_sent": {"temperature": self.temperature}}
        return dict(self._info)

    def caption(self, image_path, keep_alive=None):
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
        last = None
        for attempt in range(self.cfg.get("retries", 5)):
            t0 = time.time()
            try:
                resp = self.client.generate(model=self.cfg["model"], prompt=self.cfg["instruction"], images=[img_b64],
                                            options={"temperature": self.temperature}, keep_alive=keep_alive)
                text = (resp.response or "").strip()
                words = len(text.split())
                chars = len("".join(text.split())); cjk = len(CJK_RE.findall(text)); cjk_share = (cjk / chars) if chars else 0.0
                limit_chars = self.cfg.get("limit_chars")          # E2: the instruction's character budget (D15); None for English cells
                meta = {"caption_time_s": round(time.time() - t0, 2),
                        "caption_ollama": {k: getattr(resp, k, None) for k in
                                           ("done_reason", "total_duration", "load_duration", "prompt_eval_count", "prompt_eval_duration", "eval_count", "eval_duration")},
                        "caption_words": words, "caption_chars": chars, "caption_cjk_share": round(cjk_share, 3),
                        "caption_flags": {"empty": chars == 0, "over_50_words": words > 50, "refusal": bool(REFUSAL_RE.search(text)),
                                          "length_cutoff": getattr(resp, "done_reason", None) == "length",
                                          **({"over_limit_chars": cjk > limit_chars, "not_cjk": cjk_share < 0.5} if limit_chars else {})},
                        "caption_attempts": attempt + 1}
                if words == 0 and self.log:
                    self.log.warning("empty caption for %s (attempt %d)", image_path, attempt + 1)
                return text, meta
            except Exception as e:  # noqa: BLE001
                last = e
                wait = 5 * (attempt + 1)
                if self.log: self.log.warning("ollama error %r on %s; retry in %ds", e, image_path, wait)
                time.sleep(wait)
        raise RuntimeError(f"ollama failed after retries: {last!r}")

    def unload(self):
        """keep_alive=0 with no prompt unloads the model (SPEC §8)."""
        try:
            self.client.generate(model=self.cfg["model"], keep_alive=0)
        except Exception as e:  # noqa: BLE001
            if self.log: self.log.warning("unload request failed: %r", e)

    def loaded_models(self):
        try:
            return [m.model for m in self.client.ps().models]
        except Exception:  # noqa: BLE001
            return None
