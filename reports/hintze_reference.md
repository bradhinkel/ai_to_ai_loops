# Hintze et al. T=0.9 reference data (comparison baseline for A0)

Downloaded 2026-10-16 from figshare 30553604, file `temps_0.9.zip` (775 MB, file id 59352803), extracted to `data/hintze_figshare/temps_0.9/` (git-ignored). The other six temperatures are available as separate zips (687 to 996 MB each).

## What is in it
| Folder | Contents | Notes |
|---|---|---|
| `mosaics/` | 100 JPEGs, 5120x5120, one per run | 10x10 grid of 512x512 tiles, row-major, tile i = image at step i (0 to 99). This is the complete image record. |
| `logs/` | 100 CSVs, `run_id,rep_id,step,prompt` | step 0 = seed prompt; step k = LLaVA caption of the step k-1 image (= prompt for image k). 88 runs have all 100 rows; 9 have 99, one 98, one 96 (run 094), one 27 (run 096). |
| `images/` | 246 loose PNGs, 512x512 | Leftovers, not a full record: step-99 images for 20 runs, plus partial trajectories for runs 094, 096, 098. |

Checks done:
- Tile order verified visually on runs 000 and 096 (climber at step 0, chalet at step 99) and against the captions of run 000 (caption k describes tile k-1).
- Run 019's mosaic has blank final tiles; the loose step 97 to 99 PNGs fill them (the subset script falls back to those).
- Run 096's CSV and loose PNGs are a different, partial trajectory from its mosaic (same seed prompt, different path). Treat run 096's captions as unpaired with its mosaic.
- Hintze's captions are long: 9,812 captions, mean 88.8 words, median 86, max 330, only 7% at or under 50 words. The 50-word instruction was evidently not enforced by truncation. Confirm against the OSF code before deciding whether A0 truncates (SPEC §5 assumes the A0 pipeline truncates).

## Documentation subset (`reports/hintze_reference/`)
- `trajectories.jpg`: 8 runs (000, 010, ... 070) at steps 0, 1, 5, 10, 25, 50, 75, 99. Shows the drift from the seed into an attractor and how little changes between steps 50 and 99.
- `endpoints_step099.jpg`: step-99 image of all 100 runs, the attractor set to compare A0-core's contact sheet against.
- `captions.md`: seed prompt and captions at the sample steps for the 8 runs.
- `run_RRR/step_NNN.jpg`: the individual tiles.

Rebuild with `.venv/bin/python analysis/hintze_reference_subset.py`. Once A0 is done the full zip and extraction can be deleted; the subset is in git.
