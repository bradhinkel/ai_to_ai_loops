# papers/

Public write-ups and the figures made for them. Everything here is a working draft by Brad Hinkel with Claude as collaborator; the numbers are rebuilt from `runs/` by the scripts in `analysis/`.

## Write-ups
(to be added as PDF exports; the drafts live as Claude Docs until then)
- Gravity in AI-to-AI loops — the image loops: replication of Hintze et al., residence and escape hazards, who owns the attractors, instruction and language, the failed rejection intervention.
- Bias in AI-to-AI loops — what the loop does to seeded gender, age and skin tone (E6).
- Text loops: wells, the birthday law and model menus — the story loop on Claude, Mistral and Qwen (E3).

## figures/
Endpoint contact sheets made by `analysis/endpoint_sheets.py`: every image is step 99 of 100 for one trajectory, at native 512 px, numbered by seed.

| file | run | what |
|---|---|---|
| `a0_core_endpoints_10x10.pdf` | a0_core | all 100 endpoints of the SDXL + LLaVA replication |
| `e2_qz_endpoints_10x10.pdf` | e2_qz | all 100 endpoints of Hunyuan-DiT + Qwen2.5-VL with the Chinese instruction |
| `a0_core_endpoints_6x6.{pdf,jpg}` | a0_core | trajectories 0–35, for web use |
| `e2_qz_endpoints_6x6.{pdf,jpg}` | e2_qz | trajectories 0–35, for web use |

Rebuild: `python analysis/endpoint_sheets.py --run <run> --grid 10 --title "..." --subtitle "..." --footer "..." --out papers/figures/<run>_endpoints_10x10`
