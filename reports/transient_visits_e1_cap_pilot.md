# Transient visits: are the new cells' attractors present as intermediate states of A0? (2026-10-19)

Brad's question: attractors that show up in the E1 cells may also have appeared in A0, as states that were visited but not stable, or less prevalent. We keep every intermediate image and record (A0-pilot 2,000, A0-core 10,000, E1-cap pilot 2,000 PNGs + JSON; Hintze's T = 0.9 data as 10×10 step mosaics per run plus 246 full-size images), and DINOv2 embeddings of every step are cached, so this is a direct scan: `analysis/transient_visits.py` (method in its docstring; CLIP not used). Tables and sheets in `reports/visits_e1_cap_pilot_in_a0_core/` and `reports/visits_a0_core_in_e1_cap_pilot/`.

## E1-cap pilot attractors scanned through all 10,000 A0-core steps (radius floor 0.20)
| E1-cap pilot probe | visited by A0 trajectories | stayed | transient | what the sheet shows |
|---|---|---|---|---|
| Gilded ballroom with set tables (2 members) | 9 | 0 | 9 | A0 passes through near-identical ballrooms (nearest 0.09, steps 12–98) on its way to, or inside, the palatial-salon basin; it never ends there. |
| Luxury bathroom with free-standing tub (4) | 3 | 0 | 3 | A0 trajectories 19, 63, 84 show the same marble bathroom at steps 92, 49, 9 (nearest 0.08) and leave; the longest stay is 7 steps. |
| Canyon with lone tree (1) | 2 | 0 | 2 | brief (1 step). |
| Bare trees on islands under a lavender sunset (5) | 0 | 0 | 0 | never within radius (nearest 0.28). A0's closest states are bare trees in mist or snow, a different palette and composition. |
| Cherry-blossom pond, moss cottage, forest staircase, ballerinas, bride, pagoda | 0 | 0 | 0 | not visited (nearest 0.21–0.54). |

## A0-core archive attractors scanned through all 2,000 E1-cap pilot steps
| A0 probe (archive cluster) | visited by pilot trajectories | stayed | transient | what the sheet shows |
|---|---|---|---|---|
| Gothic cathedral nave (r 0.20) | 2 of 20 | 0 | 2 | trajectory 8 is a full cathedral at step 85 (distance 0.05) and trajectory 2 at step 29; both leave, dwell up to 24 steps; trajectory 8 ends as a bathroom. |
| Gold-and-blue palatial salon (r 0.32) | 4 | 0 | 4 | visited for up to 16 steps, none stay. |
| Luxury bedroom (r 0.33) | 2 | 0 | 2 | brief. |
| Victorian house, castle, people-and-art | 0–1 | 0 | 0–1 | not reached. |
| Catch-all landscapes (r 0.79) | 20 | 9 | 11 | the radius is too wide to mean anything; treated as "no attractor" as in the A0 report. |

## Reading
- Brad's speculation holds for the interiors family. The ballroom and the bathroom that E1-cap settles into exist inside A0 as transient states (9 and 3 trajectories visit them, none stay); under LLaVA they drain into the gold-and-blue salon, under Qwen they are stable endpoints. Conversely A0's cathedral and salon are visited by Qwen trajectories, sometimes for 16–24 steps, and then abandoned.
- The lavender-trees basin, the largest in the pilot, is genuinely new: no A0 step comes within radius, and the nearest A0 states are compositionally different.
- So the pilot's picture is two kinds of difference: a shared landscape of interior states whose *stability* depends on the captioner, and at least one basin that only the Qwen loop reaches. The E1 report should separate these (shared-but-restabilised vs new) rather than report a single overlap number; the core runs (n = 100) will make the counts meaningful.
- Caveat: distances are DINOv2 cosine with a 0.20 floor; probes with 1–2 members have no real radius. The sheets show the nearest images regardless of threshold.
