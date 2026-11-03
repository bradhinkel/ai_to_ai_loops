# Research programme: AI-to-AI loops as an instrument for a model's defaults (Brad Hinkel, drafted 2026-11-03)

This turns the project's thesis and Brad's four questions into a structured process. It sits above SPEC.md / SPEC2.md (which define arms) and below nothing; every new arm should be traceable to one of the questions below.

## Thesis
An AI-to-AI loop removes the seed within a few steps and leaves only what the model produces under minimal constraint: its default themes, ideas and biases. Image loops show this clearly (a sheet of 100 endpoints is the result); text loops follow the same model with more wells, each harder to detect but as specific once found (the shoebox of letters). The loop is therefore an instrument, and the programme is about making it a good one: calibrated, reproducible, and connected to the model's ordinary behaviour.

## The four questions, and what answers each
| | question | instrument | measure | first study |
|---|---|---|---|---|
| Q1 | Can the defaults and biases be measured accurately? demographic, cultural, political | image loop with attribute seeds (E6); essay loop with contested-topic seeds; D probe for the theme menu | attribute survival hazards; position survival (does the seed's stance survive or flip, and to what); menu composition by a blinded judge, calibrated against human coding (κ) | E6 done (κ 0.7–0.8); essay pilot running; D menus for Haiku and Mistral done |
| Q2 | Where do they come from? pretraining data, post-training (RL/instruction tuning), the loop's own construction | the same loop on base vs instruct checkpoints of open models (Qwen, Mistral, Llama, OLMo); instruction-wording ablations; language ablation (E2) | change in the well list / menu between checkpoints; menu stability across instruction paraphrases; wells traceable to data (OLMo's open corpus) | instruction ablation partly done (summary width, theme bottleneck); base-vs-instruct not started |
| Q3 | Do the defaults appear in ordinary use, not only in a Markov chain? | one-shot baselines (E6 one-shot prior); long single conversations; free-generation frequency of a well's plot under ordinary prompts | distance between loop endpoints and one-shot outputs; rate at which an ordinary "write a story about X" lands in a known well; drift toward the menu over a long chat | E6 one-shot baseline done; text not started |
| Q4 | Can they be controlled or mitigated? | selection pressure in the loop (OMNI-style interestingness judge, Phase 2); prompt and decoding controls; small fine-tunes on open models | time-to-first-well, well occupancy and menu entropy under each control, against the uncontrolled loop | not started (SPEC2 §5–6 designs exist) |

## The process for every study (what has worked so far, made explicit)
1. **Question → arm.** Name which of Q1–Q4 the arm serves and what result would change what we do next (the decision rule). An arm that cannot change a decision is not run.
2. **Prediction before data.** Thresholds in `predictions.md`, in Brad's words first, then operationalised; never edited after results. The scorecard (about a third fail) is part of the record and the pitch.
3. **Instrument first, then scale.** Smoke (2 × 3), pilot (20 seeds), then the sized cell. Size from the birthday arithmetic: with W wells the per-pair sharing rate is about 1/W, so sharing pairs grow with n²; 100 seeds see W ≈ 150; 20 seeds see W ≈ 5 (the D probe).
4. **Separate steering from grading.** The loop model never grades itself; CLIP steers and MiniLM/DINOv2 grade; the theme judge is a different model, blinded to seed, step and model, calibrated against Brad's hand coding.
5. **Two samples before a claim.** A well list is a property of the model only if a second sample (fresh step 0, same seeds) reproduces it (E3-S2, running). A bias claim needs the counter-stereotypical and stereotypical seeds in the same cell.
6. **Gate report, push, pause.** `reports/<arm>.md` leads with pass/fail against the prediction; every run's records are append-only and pinned; GitHub is pushed at every gate.
7. **Cross-model matrix as the unit of comparison.** Each instrument is run on the same seed set across models (Haiku, Sonnet, Mistral, Qwen; Opus/Fable and other vendors when funded), so that "this is Haiku's menu" is always read against "this is Mistral's".

## Programme over the next eight weeks (order, each needing its prediction)
1. **Finish the text-loop instrument (Q1 measurement).** E3-S2 second sample; projections; essay pilot; D cells on Qwen and Sonnet; Mistral and Qwen 100-seed cells (RunPod). Output: the text-loop article (Hintze's loops with a different set of attractors) and the Anthropic / OpenAI credit requests for Sonnet, Opus, Fable, GPT and Gemini cells.
2. **Bias on the essay loop (Q1, cultural and political).** Seeds: 20 contested topics × 2 framings each (for / against), position-survival measure, Haiku first; then the same on Mistral and Qwen. The E6 analysis pattern (hazard of losing the seeded position, what replaces it, one-shot baseline) transfers directly.
3. **Sources (Q2).** Base vs instruct on one open model pair (Qwen2.5 7B base vs instruct, or Mistral 7B v0.3 base vs instruct) with the story loop and the D probe: does the menu exist in the base model, and does post-training narrow it? Instruction-wording ablation (five paraphrases of the expand instruction) to bound how much of the menu is the prompt's.
4. **Ordinary use (Q3).** Free-generation frequency: 500 ordinary story requests across varied topics, judged against the known Haiku wells and menu; a long-conversation drift test.
5. **Control (Q4, image loops, the pod).** OMNI-style interestingness judge as a selector among k candidates per step (SPEC2 §5), measured by time-to-first-well and endpoint entropy; the D&D / caption-rejection arms as the comparison.

## Outputs and audiences
- Papers: gravity (Hintze), bias (Caliskan), text attractors (new; Haiku/Mistral/Qwen, image bias as the further direction). Working drafts in Brad's voice; collaborators invited to correct.
- Funding: Anthropic External Researcher Access Program and OpenAI Researcher Access Program (Q1 cross-vendor matrix); Gemini Academic Program via a university partner.
- Public: LinkedIn article (the broader thesis, high-level results); repository public with records, configs and the predictions scorecard; Zenodo DOI for `runs/`.

## Risks and standing cautions
- MiniLM truncates at 256 word pieces: text wells are found on the story's opening; summaries are embedded in full as the check.
- Names and places carry two-thirds of the distance between text trajectories; anonymised embedding is the standard for text atlases, raw is reported beside it.
- The D probe has no memory (half-life 1–2); it measures a stationary menu, not gravity. Gravity claims rest on the 50-word loop.
- The judge is a Claude model judging Claude's stories; calibration against Brad's hand coding and a second judge (Sonnet, or a non-Anthropic model when funded) bound the circularity.
- Costs: Haiku 100 × 100 ≈ $11 with judge; Sonnet ≈ $145; 7B models ≈ 1.5 laptop-days or ≈ $12 on a pod per 100-seed cell. Brad's approval precedes any cell over $10.
