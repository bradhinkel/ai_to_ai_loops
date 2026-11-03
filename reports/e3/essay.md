# E3-E essay-loop pilot: e3_e_haiku

Predictions: predictions.md "E3-E essay-loop pilot" (2026-11-03), E1–E4. Atlas rules as E3-S (k 40); raw unless stated.

**E1 (rate similar to story cells): fails** — raw shared wells 0 (persistent 2), anonymised shared 0 (persistent 2), anonymised rate 0.0000 (0 of 190), raw rate 0.0000, nn-other 0.562 (anon 0.509), within 0.15 0.000 (anon 0.000); fails upward: False.
**E2 (longer memory): fails** — half-life None, own-seed identification at 10 / 25 / 50 / 99: 0.95 / 0.9 / 0.8 / 0.8.
**E3 (drift to a few abstract domains): fails** — step-0 top domain share 0.2; late (steps 50–99) modal domain history 0.24; abstract share step 0 0.15 → late 0.59; named direction (society/politics or philosophy/religion): fails; no-menu clause (<0.25): True. Judge: 1997 essays coded, 3 malformed.
**E4 (format): holds** — median words at step 99 517, summaries within 50 words 0.79, refusal flags 0 (the flag is the D19 heuristic; flagged examples: []), Vendi story 99 16.2, summary 99 17.2.

![essay](e3/essay.png)

## Domain and subject kind

| domain | step 0 | steps 50–99 |
|---|---|---|
| science_and_nature | 0.20 | 0.16 |
| technology | 0.05 | 0.05 |
| history | 0.20 | 0.24 |
| society_and_politics | 0.00 | 0.03 |
| arts_and_culture | 0.05 | 0.04 |
| philosophy_and_religion | 0.10 | 0.17 |
| health_and_body | 0.10 | 0.06 |
| economics | 0.05 | 0.10 |
| mathematics | 0.15 | 0.12 |
| places | 0.10 | 0.00 |
| other | 0.00 | 0.02 |

| field (steps 50–99) | shares |
|---|---|
| subject kind | abstract 0.59, concrete 0.41 |
| stance | argues_a_position 0.78, descriptive 0.22 |
| tone | hopeful 0.48, cautionary 0.19, neutral 0.15, celebratory 0.11, critical 0.07 |
| mentions AI/computing | no 0.93, yes 0.07 |
| mentions environment/climate | no 0.76, yes 0.24 |

## Each trajectory: seed topic → step 50 → step 99 (judge topic sentences)

| traj | seed (first words) | step 0 domain | step 50 topic | step 99 domain / kind | step 99 topic |
|---|---|---|---|---|---|
| 0 | The Age of Discovery (c. 1418 – c. 1620), also known as the  | history | The far-reaching exchange of crops, diseases, and peoples between the Americas and Eurasia after 1492, with its mixed consequences. | history / concrete | Textbook framing of the early global exchange of goods hides disease, forced labor, and cultural destruction. |
| 1 | An aircraft or aerial vehicle is a vehicle that can fly by g | technology | Hybrid aircraft promise regional air service, but adaptive software requires continuous monitoring, bounded adaptation, and shared governance to remain safe. | technology / concrete | Adaptive software in hybrid-electric regional aircraft challenges certification, requiring monitoring, bounded adaptation, backup controls, accountability, and transparency. |
| 2 | Algebra is a branch of mathematics that deals with abstract  | mathematics | Teaching algebra as a language of relationships and reasoning rather than memorized procedures. | mathematics / abstract | How teaching for meaning, multiple representations, and reframing errors can reduce anxiety about learning algebra. |
| 3 | An allergy is an exaggerated immune response where the body  | health_and_body | Why allergies have risen in wealthy nations and how restoring early microbial exposure could help prevention. | health_and_body / abstract | Why allergic diseases have risen in wealthy nations and how environmental and lifestyle changes might reverse the trend. |
| 4 | Ancient Egypt was a cradle of civilization concentrated alon | history | How the annual Nile flood and the agricultural surplus it enabled helped build ancient Egyptian society and its institutions. | history / concrete | How a predictable river, record-keeping, grain stores, and divine kingship together sustained a long-lived state through repeated fragmentation. |
| 5 | Ancient Greece (Ancient Greek: Ἑλλάς, romanized: Hellás) was | history | Athenian democracy's exclusions and the trial of Socrates, and what they teach modern democracies about citizenship and free inquiry. | history / concrete | Athenian democracy's inclusions, exclusions, and the trial of a critic, and what they teach modern democracies. |
| 6 | Anger, rage, or its extreme counterpart, wrath (UK:  ROTH; U | health_and_body | How anger works as a signal of threatened values, and how expressing it constructively strengthens relationships. | health_and_body / abstract | How anger signals threatened values, and why naming them calmly, rather than suppressing or exploding, builds trust. |
| 7 | Animal husbandry is the branch of agriculture concerned with | economics | Cheap meat's hidden costs to water, climate, animals, and antibiotic effectiveness, and how pricing should reflect them. | economics / concrete | A proposed per-pound fee on meat to cover external harms, with equal rebates returned to households. |
| 8 | The Arabic numerals are ten digits (0, 1, 2, 3, 4, 5, 6, 7,  | mathematics | How the Hindu-Arabic numeral system emerged gradually across India, the Islamic world, and Europe, and spread into global use. | mathematics / concrete | How the Hindu-Arabic numeral system developed collectively across civilizations over more than a millennium, through exchange and transmission. |
| 9 | Archimedes of Syracuse ( AR-kih-MEE-deez; c. 287 – c. 212 BC | mathematics | How a third-century BCE Greek thinker united mathematical theory with practical engineering and physical discovery. | mathematics / abstract | Whether mathematics is invented or discovered, and how its success in describing nature bears on that question. |
| 10 | Atoms are the basic particles of the chemical elements and t | science_and_nature | How scientists should respond to anomalous results, balancing skepticism with openness to genuine discovery through replication. | science_and_nature / abstract | How science balances openness to anomalies with skepticism toward extraordinary claims, illustrated by contrasting historical cases. |
| 11 | Beauty is commonly described as a feature of objects that ma | philosophy_and_religion | Whether beauty is a measurable property, a private feeling, or an achievement of trained perception of structure. | philosophy_and_religion / abstract | Whether beauty is objective, merely private taste, or a collective human achievement shaped by perception, judgment, and debate. |
| 12 | The Bible is an anthology of religious texts that are centra | philosophy_and_religion | Reading the collection of biblical writings by genre, with attention to context, as a faithful and humble approach to interpretation. | philosophy_and_religion / abstract | Five commitments that shape a humble, lifelong posture of listening to Scripture and being transformed by it. |
| 13 | Brazil, officially the Federative Republic of Brazil, is the | places | Why the rainforest matters for rainfall, carbon storage, and Indigenous communities, not as the planet's oxygen source. | science_and_nature / concrete | Why the rainforest's oxygen role is overstated and why its carbon, water, and biodiversity value better justify protection. |
| 14 | Bronze is an alloy consisting primarily of copper, commonly  | science_and_nature | How the alloy bronze reshaped ancient farming, power, warfare, and trade, helping drive the growth of complex societies. | history / concrete | How the alloy bronze reshaped ancient agriculture, trade, writing, and social hierarchy, and how those hierarchies outlasted the Bronze Age. |
| 15 | The Bronze Age is an archaeological and anthropological term | history | How pursuing efficiency without redundancy leaves societies fragile, and why governments should maintain reserves and diversify supply. | economics / abstract | How regulators should design outcome-based resilience standards for systemically important firms, with flexible methods and rigorous verification. |
| 16 | Calligraphy (from Ancient Greek  καλλιγραφία (kalligraphía)  | arts_and_culture | The enduring value of handwriting for expressing identity, supporting thought, and nurturing personal connection alongside digital tools. | other / abstract | Recursive writing instruction that treats revision and errors as ways of discovering meaning, not just linear polishing. |
| 17 | Canada is a country in North America. Its ten provinces and  | places | Whether national pride should be grounded in an honest accounting of a country's historical injustices. | society_and_politics / abstract | Acknowledging historical injustices strengthens national identity more than celebrating achievements alone, since honest pride rests on truth. |
| 18 | A carbohydrate () is a sugar (saccharide), a polysaccharide  | science_and_nature | How the arrangement of identical molecular building blocks, rather than their composition, determines biological structure and function across biology, medicine, and materials. | science_and_nature / abstract | Progress comes from rearranging existing materials and resources rather than discovering new ones. |
| 19 | The cat (Felis catus), also called domestic cat and house ca | science_and_nature | How lasting love is sustained through commitment and everyday care rather than initial passionate feeling. | philosophy_and_religion / abstract | How passionate love fades into embers and how faithfulness, repair, and everyday care sustain lasting love. |

## Step-99 summaries

- traj 0: Textbooks often portray the Columbian Exchange as mutual enrichment, obscuring the catastrophe behind it: disease, coerced labor, enslavement, and cultural destruction that killed millions. Indigenous peoples nonetheless resisted and endured. Honest teaching must acknowledge both exchange and suffering, including who profited and who paid.
- traj 1: Hybrid-electric regional aircraft could connect remote communities to clinics, markets, and schools by making low-volume routes economically viable. However, adaptive software that changes over time challenges traditional certification. Regulators should require continuous monitoring, bounded adaptation, independent backup controls, clear accountability, and transparent oversight to ensure innovation and safety advance together.
- traj 2: Algebra anxiety often stems from memorizing procedures without understanding them, leaving students helpless when problems look unfamiliar. Remedies include teaching for meaning, using multiple representations, and treating errors as diagnostic clues. Together, these build reasoning-based confidence that counters anxiety.
- traj 3: Allergic diseases like asthma and eczema have risen sharply in wealthy nations, likely due to environmental and lifestyle changes. Reduced microbial exposure, disrupted gut microbiomes, and urban pollution weaken immune development. Solutions include limiting antibiotics, supporting breastfeeding, improving diet, and designing cities with green space and cleaner air.
- traj 4: Ancient Egypt lasted about three millennia due to four reinforcing pillars: a predictable Nile flood, a literate scribal bureaucracy, state grain reserves, and divine kingship. Together they let Egypt recover from fragmentation and restore unity repeatedly.
- traj 5: Athens pioneered direct democracy, using assemblies, lot-chosen officials, and large jury panels, yet excluded women, slaves, and resident foreigners. Its conviction of Socrates revealed majority rule's danger to dissent. Modern democracies must broaden participation, protect free inquiry through institutions, and cultivate civic virtue.
- traj 6: Anger is not an enemy but a messenger signaling that something we value is threatened. Suppressing it breeds resentment, while exploding derails resolution. The healthier path is to pause, identify the underlying value, and express it calmly. Handled well, anger deepens trust and connection.
- traj 7: A per-pound meat fee would force producers to pay for the costs their operations impose, including water pollution, antibiotic-resistant infections, and dangerous working conditions. Returning revenue to households through equal rebates would protect low-income families, and dedicated funding would target the harms directly.
- traj 8: The Hindu-Arabic numeral system developed over more than a millennium through collective effort. Indian mathematicians created positional notation and zero as a number, Islamic scholars in Baghdad refined and transmitted it, and Fibonacci introduced it to Europe. Its origins reflect shared knowledge, not a lone genius.
- traj 9: Mathematics is both invented and discovered. Its methods, notations, and axioms are human creations, yet within chosen frameworks its results are fixed and independent of will. This explains why mathematics, built by people, so often reveals the structure of the natural world.
- traj 10: Science requires balancing openness to unexplained anomalies with skepticism toward extraordinary claims. Mercury's orbital anomaly, carefully measured and kept open as a problem, led to Einstein's general relativity. Cold fusion, announced without adequate testing, collapsed under replication failures. Rigorous, independent testing distinguishes genuine discoveries from illusions.
- traj 11: Beauty is neither a fixed objective property nor mere private taste. It is a collective achievement: shared human perception provides the foundation, cultivated judgment refines it, and public debate across generations tests and revises it over time.
- traj 12: Faithful Bible reading is a humble, lifelong listening posture, not mere fact-extraction. It rests on five commitments: attending to genre, balancing literal and allegorical readings, reading within the church's tradition, centering on Christ, and pursuing transformation over information. Together they reshape readers to love what God loves.
- traj 13: The "lungs of the planet" metaphor about the Amazon is scientifically misleading. Mature forests produce roughly as much oxygen as they consume, and most atmospheric oxygen comes from ocean phytoplankton. The Amazon still deserves protection for its carbon storage, rainfall regulation, and biodiversity, which are measurable and more defensible reasons.
- traj 14: Bronze, a copper-tin alloy used from around 3300 BCE, transformed ancient societies. Stronger farming tools created agricultural surpluses, enabling craft specialization and urban life. Tin scarcity drove long-distance trade, which likely contributed to writing. Control of metal concentrated wealth and power among elites, a hierarchy that persisted even after iron replaced bronze.
- traj 15: Resilience benefits third parties, so markets underinvest in it, justifying regulation. Prescriptive rules, however, become outdated and encourage box-ticking. Better is outcome-based regulation: set survival targets scaled to systemic importance, let firms choose how to meet them, and verify through stress tests, audits, and disclosure.
- traj 16: Writing instruction often teaches a linear model: plan, draft, revise, edit, publish. Real writing is recursive, with discovery happening throughout. Instruction should treat revision as rethinking meaning, balance structure with exploration, and read errors as diagnostic clues revealing what students are attempting.
- traj 17: Canada's pride is sound only when it is honest. The transcontinental railway, residential schools, the wartime internment of Japanese Canadians, and the refusal of the MS St. Louis all reveal injustices. Confronting them strengthens national identity, which rests on truth and a commitment to do better.
- traj 18: Progress often comes not from new materials but from rearranging familiar ones. Carbon becomes diamond or graphite, and glucose becomes starch or cellulose, purely through changed structure. Engineers now design metamaterials and simulate configurations on computers. The essay argues that societies too should rethink how existing elements are organized, since the future may belong to those who rearrange what they already have.
- traj 19: Passion's intense early blaze inevitably cools into embers, which is natural rather than a failure. Lasting love rests on three foundations: faithfulness that creates security, humble repair after conflict, and everyday care. Together, these sustain a steadier warmth than passion alone.
