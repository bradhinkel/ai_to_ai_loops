# E3-DS: Sonnet theme-bottleneck cell `e3_d_sonnet` against predictions.md "E3-DS" (2026-11-05)

**DS1 (shared menu with Haiku): holds** — Haiku moral judge on 1000 late stories: fit to one of Haiku's five morals 0.82 (needs ≥ 0.5), morals above 0.10: 4 (needs ≥ 2); hand-read top-five overlap 3 (needs ≥ 2).

| Haiku D moral | share of Sonnet late stories |
|---|---|
| Grief is eased by small kindnesses from a community. | 0.17 |
| Estranged siblings or relatives reconcile through shared grief; pride gives way to humility and honesty. | 0.11 |
| Kindness ripples outward through strangers, each passing it on. | 0.40 |
| A shared crisis dissolves old grudges between neighbours. | 0.00 |
| Grief is softened through family rituals and shared memory. | 0.15 |
| none of these | 0.17 |

**DS2 (D dynamics): fails** — half-life 1 (≤ 3), raw median dwell 1.0 (1), clusters per trajectory 6.0 (7–12), free steps 0.75 (≥ 0.6), anonymised shared wells 5 (≥ 5), rate 0.068 (0.10–0.30).

**DS3 (domestic shape): fails** — interpersonal + internal 0.71 (≥ 0.6), home + small town 0.54 (≥ 0.5), hopeful 0.72 (≥ 0.8), family secondary 0.34 (≥ 0.4).

**DS4 (confession moral): fails** — late theme sentences matching the confession/honesty rule 0.13 (≥ 0.15); among stories the Haiku judge scored "none" 0.27 (≥ 0.5, i.e. the top none-moral); reference D cells: e3_d_haiku 0.24, e3_d_mistral 0.00.

## Cells

| cell | half-life | raw shared / rate | anon shared / rate / W-hat / max mult | clusters per traj / median dwell (raw) | free steps (raw) | anon dwell ≥ 5 share |
|---|---|---|---|---|---|---|
| e3_d_sonnet | 1 | 0 / 0.000 | 5 / 0.068 / 14.6 / 4 | 6 / 1.0 | 0.75 | 0.10 |
| e3_d_haiku | 1 | 0 / 0.000 | 7 / 0.184 / 5.4 / 5 | 12 / 1.0 | 0.66 | 0.14 |
| e3_d_mistral | 2 | 0 / 0.000 | 8 / 0.205 / 4.9 / 6 | 7 / 1.0 | 0.74 | 0.18 |

## Judge field shares, steps 50–99

| field | e3_d_sonnet | e3_d_haiku | e3_d_mistral |
|---|---|---|---|
| interpersonal_plus_internal | 0.71 | 0.85 | 0.01 |
| home_plus_small_town | 0.54 | 0.67 | 0.62 |
| hopeful | 0.72 | 0.80 | 0.98 |
| family_secondary | 0.34 | 0.71 | 0.07 |
| social | 0.15 | 0.11 | 0.59 |
| artist_lead | 0.02 | 0.01 | 0.50 |
| woman | 0.82 | 0.75 | 0.47 |
| death | 0.60 | 0.68 | 0.07 |
| reconciliation | 0.26 | 0.61 | 0.12 |
| modal tuple | older_adult × internal × hopeful 0.15 | middle_aged × interpersonal × hopeful 0.28 | unclear × social_or_community × hopeful 0.42 |
| conflict | internal 0.53, interpersonal 0.18, social_or_community 0.15, external_physical 0.09 | interpersonal 0.58, internal 0.28, social_or_community 0.11, external_physical 0.03 | social_or_community 0.59, external_physical 0.32, none_or_unclear 0.08, internal 0.01 |
| setting | home_interior 0.42, city 0.28, small_town_or_village 0.12, rural_or_farmland 0.06 | home_interior 0.58, rural_or_farmland 0.12, small_town_or_village 0.09, institution 0.08 | small_town_or_village 0.62, city 0.24, wilderness_or_mountain 0.05, other_or_unclear 0.04 |
| secondary | stranger 0.31, friend 0.22, sibling 0.14, child 0.12 | sibling 0.53, friend 0.14, parent_or_grandparent 0.09, other 0.08 | other 0.61, authority_or_mentor 0.08, stranger 0.08, none 0.07 |
| lead_role | other_or_unclear 0.45, worker_or_tradesperson 0.21, caregiver_or_parent 0.16, retired 0.10 | other_or_unclear 0.65, caregiver_or_parent 0.14, worker_or_tradesperson 0.10, retired 0.04 | artist_or_craftsperson 0.50, leader_or_official 0.16, other_or_unclear 0.14, worker_or_tradesperson 0.08 |

## Theme sentences the Haiku judge scored as none of Haiku's five (first 40 of 175)

- Small, unthinking acts of kindness can ripple through time, returning unexpectedly to help the giver when she needs it most.
- Even after decades together, assuming you know someone can hide their true wishes, and honest conversation can renew intimacy by revealing who they really are.
- Love grows deeper when partners stop sacrificing silently to please each other and honestly share their true wants, even after decades of well-meant pretending.
- Even in long marriages, unspoken efforts to please each other can hide true desires, and honest disclosure can renew intimacy.
- Honest communication, rather than silently sacrificing for each other's presumed preferences, restores intimacy and lets partners truly discover one another.
- Trying to please a partner by hiding your true preferences creates distance, while honest disclosure lets you discover each other and yourselves anew.
- Real intimacy requires honestly revealing your true preferences rather than pretending to share someone's tastes to keep them happy.
- Real intimacy requires honestly sharing who you are, because pretending to match someone's preferences creates distance rather than closeness.
- Real intimacy requires honest self-disclosure, because hiding your true preferences to please someone prevents them from ever truly knowing or connecting with you.
- Real intimacy begins when we stop performing an agreeable version of ourselves and risk being honestly known, flaws and preferences included.
- Real intimacy requires abandoning the effort to be agreeable and risking honesty, because only an authentic self can be truly known and loved.
- Genuine intimacy requires dropping the habitual agreeableness that protects us, because being honestly seen, flaws and all, is the only way to truly be loved.
- Real intimacy requires honest self-expression, because constant agreeableness hides who we are and leaves love directed at a false version of us.
- Real intimacy requires showing your true, imperfect self rather than molding yourself to please a partner, because only then can you be truly loved.
- Real intimacy comes from showing your true, imperfect self rather than suppressing it to be easily loved.
- True intimacy comes only when we drop our curated, agreeable performances and let others see our messy, honest selves.
- Real connection comes when we drop our polished facades and admit our flaws, since vulnerability invites others to be honest and makes a place feel like home.
- Admitting our struggles and imperfections, rather than hiding behind a flawless facade, dissolves isolation and invites the genuine connection and support we crave.
- Real comfort in grief comes from quiet, patient presence that lets pain be felt, not from advice, platitudes, or pressure to appear strong.
- Reconciliation grows through small, quiet acts of care that rebuild trust more effectively than words can.
- A sincere apology takes full responsibility without excuses or demands for forgiveness, and it accepts that the hurt person decides when and whether to heal.
- A sincere apology takes full responsibility without demanding forgiveness, leaving the injured person free to decide how, or whether, to respond.
- True accountability means admitting harm without demanding forgiveness, which restores the wronged person's truth and leaves her free to decide how to respond.
- A sincere, unconditional admission of wrongdoing can restore someone's self-trust and return to them the freedom to decide about forgiveness on their own terms.
- Being honestly validated after being gaslit can restore a person's trust in her own judgment and give her the freedom to choose her own response.
- Honoring tradition means adapting it so that everyone can take part, because inclusion keeps a living tradition alive and brings families together.
- True traditions endure by adapting to include everyone, making space for each person's abilities and belonging rather than excluding anyone to preserve old rules.
- True tradition honors its purpose rather than its rigid form, and adapting it to include everyone makes it richer.
- True devotion to a tradition means honoring its purpose of welcoming and including others, even if that requires changing the rule's original form.
- True welcome means honoring the purpose behind tradition and letting newcomers contribute, so belonging is shared rather than merely bestowed.
- True welcome goes beyond polite hospitality to include newcomers as contributors, valuing what they can give and offering them a real place.
- True belonging comes not from being treated kindly but from being invited to contribute your skills and be needed by others.
- True belonging comes not from receiving charity but from contributing your skills and being needed by others as an equal.
- True belonging comes not from receiving charity but from being able to contribute your own skills and be valued for them.
- True belonging comes not from receiving charity but from being able to contribute your skills and be needed by others.
- Belonging comes not from receiving kindness but from contributing your own skills, which turns charity into mutual exchange and lets you be truly known.
- True belonging comes not from receiving charity gratefully but from contributing your own skills, which turns dependence into mutual exchange and lets others truly know you.
- Belonging comes through mutual exchange, when we offer our own gifts rather than only receiving kindness with endless gratitude.
- True belonging comes not from passively receiving kindness but from contributing and sharing mutual obligations, which turn gratitude into genuine connection.
- True belonging comes not from receiving kindness but from contributing to the shared give-and-take that makes people depend on one another.
