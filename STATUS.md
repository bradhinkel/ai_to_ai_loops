# Session handoff — 2026-10-16

Nothing built yet. Documents read; machine checked. See the questions below.

## Brad's setup to-dos (need sudo / Windows)
1. `curl -fsSL https://ollama.com/install.sh | sh` then `ollama pull llava:13b`
2. `.wslconfig`: add `memory=24GB` under `[wsl2]`, then `wsl --shutdown` (WSL was capped at 16 GB of 31 GB)
3. NVIDIA Control Panel: CUDA Sysmem Fallback Policy = "Prefer No Sysmem Fallback"

## Open questions (unanswered)
1. OSF (WGDQ4) returned 503 all day. Reimplement from the paper using figshare seed prompts/captions, or wait for OSF?
2. Move SPEC.md / CLAUDE.md / DEVIATIONS.md / predictions.md / PANEL.md from Resources/ to the project root?
3. `git init` (ignore runs/, .env)?
4. predictions.md has no A0 entry. Claude drafts one for approval, or Brad writes it?
5. Download Hintze's T=0.9 images (775 MB, figshare 30553604) or only the caption CSV logs?
6. Web UI: read-only FastAPI on localhost:8000 over runs/ and logs/, or with start/stop controls?

## Next steps once answered
venv (PyTorch cu128) → SDXL VRAM check at 512x512 → 1 trajectory x 5 steps for throughput → kill/resume test → 20-trajectory pilot.
