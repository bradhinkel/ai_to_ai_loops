# Elbow tracking table (built 2026-10-19)

Rule: knee of normalised inertia (max chord distance), KMeans n_init=10 random_state=0, k=2..min(25,n-1). Spread: 200 random 80% subsamples without replacement, same rule. Rebuilt by `analysis/elbow_table.py` after every run; the SPEC §4.3 reading since 2026-10-18 is 'matches Hintze's T=0.9 data under this rule', and this table is where variation between runs is tracked.

| Set | n | knee k (rule) | knee by kmax 15 / 20 / 30 / 40 | silhouette max (top 3) | subsample knee median [5%, 95%] |
|---|---|---|---|---|---|
| a0_pilot minilm captions | 20 | **8** | 8 / – / – / – | 6 (6, 4, 8) | 7 [6, 8] |
| a0_pilot dinov2 images | 20 | **8** | 8 / – / – / – | 6 (6, 7, 5) | 9 [7, 9] |
| a0_core minilm captions | 100 | **7** | 7 / 7 / 7 / 14 | 4 (4, 5, 9) | 8 [6, 10] |
| a0_core dinov2 images | 100 | **8** | 5 / 5 / 9 / 10 | 11 (11, 13, 9) | 7 [5, 9] |
| e1_cap_pilot minilm captions | 20 | **9** | 9 / – / – / – | 2 (2, 3, 4) | 8 [7, 9] |
| e1_cap_pilot dinov2 images | 20 | **10** | 10 / – / – / – | 10 (10, 11, 9) | 9 [8, 10] |
| Hintze T=0.9 minilm captions | 99 | **8** | 7 / 7 / 8 / 9 | 8 (8, 10, 9) | 8 [6, 10] |
