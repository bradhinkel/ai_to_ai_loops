# Escape-hazard test across the E1 2x2

Source: `reports/persistent_atlas.json` (fixed radius 0.2, dwell >= 5). A pair counts when both cells have >= 40 trajectory-steps inside the cluster. Ratio = larger hazard / smaller hazard. Brad's claim: ratios <= 2 for every pair type. Claude's: <= 2 only for same-captioner pairs.

| cluster | name | pair | pair type | hazard 1 (steps) | hazard 2 (steps) | ratio |
|---|---|---|---|---|---|---|
| 12 | ballerinas and dancers | a0_core / e1_both | nothing shared | 0.096 (83) | 0.084 (645) | 1.15 |
| 22 | luxury canopy bedroom | e1_cap / e1_gen | nothing shared | 0.268 (56) | 0.106 (66) | 2.53 |
| 13 | gothic cathedral nave | e1_cap / e1_gen | nothing shared | 0.076 (291) | 0.204 (392) | 2.70 |
| 22 | luxury canopy bedroom | a0_core / e1_gen | same captioner | 0.119 (412) | 0.106 (66) | 1.12 |
| 12 | ballerinas and dancers | a0_core / e1_gen | same captioner | 0.096 (83) | 0.151 (218) | 1.57 |
| 16 | luxury bathroom | e1_cap / e1_both | same captioner | 0.068 (425) | 0.141 (71) | 2.06 |
| 29 | gold corridor / grand hall (Hunyuan) | a0_core / e1_gen | same captioner | 0.574 (68) | 0.271 (59) | 2.11 |
| 5 | lone tree in a mirror lake | e1_cap / e1_both | same captioner | 0.119 (447) | 0.254 (248) | 2.14 |
| 27 | soccer players, painterly | a0_core / e1_gen | same captioner | 0.210 (105) | 0.068 (103) | 3.08 |
| 13 | gothic cathedral nave | a0_core / e1_gen | same captioner | 0.024 (584) | 0.204 (392) | 8.51 |
| 30 | desert dunes | a0_core / e1_cap | same generator | 0.070 (129) | 0.100 (230) | 1.43 |
| 32 | white-and-gold salon / ballroom | a0_core / e1_cap | same generator | 0.188 (589) | 0.127 (565) | 1.48 |
| 3 | gold-and-blue palatial salon | a0_core / e1_cap | same generator | 0.127 (1283) | 0.225 (182) | 1.77 |
| 12 | ballerinas and dancers | e1_gen / e1_both | same generator | 0.151 (218) | 0.084 (645) | 1.81 |
| 22 | luxury canopy bedroom | a0_core / e1_cap | same generator | 0.119 (412) | 0.268 (56) | 2.25 |
| 13 | gothic cathedral nave | a0_core / e1_cap | same generator | 0.024 (584) | 0.076 (291) | 3.15 |
| 39 | boxers in a ring | a0_core / e1_cap | same generator | 0.070 (86) | 0.018 (56) | 3.91 |
| 19 | East Asian garden, pagoda, Fuji | a0_core / e1_cap | same generator | 0.267 (60) | 0.048 (396) | 5.56 |
| 18 | pink-and-gold banquet hall | a0_core / e1_cap | same generator | 0.595 (42) | 0.078 (550) | 7.61 |

| pair type | n comparisons | median ratio | share within 2x |
|---|---|---|---|
| same captioner | 7 | 2.11 | 29% |
| same generator | 9 | 2.25 | 44% |
| nothing shared | 3 | 2.53 | 33% |
