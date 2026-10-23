# Culture judge: e2_qz vs e1_both

Judge: Claude Sonnet 5.5, image only, prompt `culture_v1` (`analysis/culture_judge.py`). Columns: images judged / with a person / with a visible face / faces read as East Asian: yes / no / ambiguous / images with any East Asian motif / setting judged east_asia / visible CJK script.

| run | step | judged | person | face | EA yes | EA no | EA ambiguous | EA yes share of faces | any EA motif | setting east_asia | CJK script |
|---|---|---|---|---|---|---|---|---|---|---|---|
| e2_qz | 0 | 100 | 78 | 52 | 0 | 17 | 17 | 0.00 | 0 | 0 | 0 |
| e2_qz | 5 | 100 | 66 | 29 | 0 | 6 | 22 | 0.00 | 12 | 9 | 1 |
| e2_qz | 20 | 100 | 53 | 7 | 0 | 1 | 5 | 0.00 | 15 | 12 | 0 |
| e2_qz | 99 | 100 | 29 | 3 | 0 | 0 | 3 | 0.00 | 26 | 19 | 0 |
| e1_both | 0 | 100 | 78 | 48 | 0 | 18 | 14 | 0.00 | 0 | 0 | 0 |
| e1_both | 5 | 100 | 74 | 28 | 0 | 7 | 18 | 0.00 | 3 | 2 | 0 |
| e1_both | 20 | 100 | 68 | 7 | 0 | 2 | 5 | 0.00 | 5 | 1 | 0 |
| e1_both | 99 | 100 | 53 | 7 | 0 | 0 | 7 | 0.00 | 17 | 4 | 0 |

- e2_qz step 0: motifs {}; regions {'none_or_abstract': 46, 'western': 30, 'other': 23, 'middle_east': 1}
- e2_qz step 5: motifs {'other_east_asian': 6, 'curved_tiled_roof': 4, 'lantern': 3, 'east_asian_dress': 3, 'ink_wash_style': 3, 'pagoda': 2, 'cjk_text_or_calligraphy': 1, 'temple_or_shrine': 1, 'cherry_blossom': 1}; regions {'none_or_abstract': 74, 'other': 12, 'east_asia': 9, 'western': 5}
- e2_qz step 20: motifs {'other_east_asian': 8, 'curved_tiled_roof': 6, 'ink_wash_style': 5, 'temple_or_shrine': 4, 'lantern': 3, 'bamboo': 3, 'east_asian_dress': 3, 'pagoda': 2, 'cherry_blossom': 1}; regions {'none_or_abstract': 74, 'east_asia': 12, 'other': 9, 'western': 5}
- e2_qz step 99: motifs {'curved_tiled_roof': 10, 'ink_wash_style': 10, 'other_east_asian': 9, 'temple_or_shrine': 6, 'pagoda': 4, 'east_asian_dress': 4, 'lantern': 4, 'cherry_blossom': 3, 'bamboo': 1, 'dragon_or_koi': 1}; regions {'none_or_abstract': 70, 'east_asia': 19, 'other': 9, 'western': 1, 'middle_east': 1}
- e1_both step 0: motifs {}; regions {'none_or_abstract': 44, 'western': 30, 'other': 26}
- e1_both step 5: motifs {'other_east_asian': 3, 'east_asian_dress': 1, 'temple_or_shrine': 1, 'lantern': 1, 'curved_tiled_roof': 1}; regions {'none_or_abstract': 67, 'western': 22, 'other': 9, 'east_asia': 2}
- e1_both step 20: motifs {'lantern': 3, 'dragon_or_koi': 1, 'cherry_blossom': 1, 'curved_tiled_roof': 1, 'temple_or_shrine': 1}; regions {'none_or_abstract': 69, 'western': 15, 'other': 12, 'africa': 1, 'south_asia': 1, 'east_asia': 1, 'middle_east': 1}
- e1_both step 99: motifs {'cherry_blossom': 14, 'temple_or_shrine': 4, 'fuji_like_mountain': 3, 'curved_tiled_roof': 3, 'pagoda': 3, 'ink_wash_style': 1}; regions {'none_or_abstract': 69, 'other': 16, 'western': 10, 'east_asia': 4, 'middle_east': 1}
