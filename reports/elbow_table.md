# Elbow tracking table (built 2026-10-20)

Rule: knee of normalised inertia (max chord distance), KMeans n_init=10 random_state=0, k=2..min(25,n-1). Spread: 200 random 80% subsamples without replacement, same rule. Rebuilt by `analysis/elbow_table.py` after every run; the SPEC §4.3 reading since 2026-10-18 is 'matches Hintze's T=0.9 data under this rule', and this table is where variation between runs is tracked.

| Set | n | knee k (rule) | knee by kmax 15 / 20 / 30 / 40 | silhouette max (top 3) | subsample knee median [5%, 95%] |
|---|---|---|---|---|---|
| a0_core minilm captions | 100 | **7** | 7 / 7 / 7 / 14 | 4 (4, 5, 9) | 8 [6, 10] |
| a0_core dinov2 images | 100 | **8** | 5 / 5 / 9 / 10 | 11 (11, 13, 9) | 7 [5, 9] |
| e1_cap minilm captions | 100 | **6** | 6 / 6 / 9 / 16 | 2 (2, 4, 3) | 8 [6, 11] |
| e1_cap dinov2 images | 100 | **8** | 6 / 6 / 9 / 11 | 26 (26, 20, 31) | 8 [6, 9] |
| e1_gen minilm captions | 100 | **11** | 8 / 11 / 11 / 11 | 36 (36, 28, 23) | 11 [8, 13] |
| e1_gen dinov2 images | 100 | **8** | 8 / 8 / 8 / 18 | 40 (40, 37, 33) | 12 [9, 15] |
| e1_both minilm captions | 100 | **7** | 7 / 7 / 11 / 11 | 3 (3, 5, 25) | 8 [6, 11] |
| e1_both dinov2 images | 100 | **8** | 8 / 8 / 14 / 14 | 33 (33, 28, 36) | 10 [8, 13] |
| Hintze T=0.9 minilm captions | 99 | **8** | 7 / 7 / 8 / 9 | 8 (8, 10, 9) | 8 [6, 10] |
