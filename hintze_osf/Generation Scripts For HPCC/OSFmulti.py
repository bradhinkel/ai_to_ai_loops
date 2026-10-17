import torch
import torchvision
import diffusers
import transformers
import accelerate
import safetensors
import scipy
import numpy as np
from diffusers import StableDiffusionPipeline, StableDiffusionXLPipeline
import pickle
import os
import base64
import csv
from PIL import Image
from io import BytesIO
import ollama
import sys

# ---------------- Model Lists ----------------
GENERATORS = [
    "stabilityai/stable-diffusion-xl-base-1.0",
    "segmind/SSD-1B",
    "runwayml/stable-diffusion-v1-5",
    "playgroundai/playground-v2-1024px-aesthetic"
]

# Which models use SDXL pipeline vs regular SD pipeline
USES_SDXL = [True, True, False, True]  # True for SDXL-based, False for SD 1.5

INTERPRETERS = [
    "llava:latest",
    "bakllava",
    "llava:13b-v1.6",
    "moondream"
]

# ---------------- Setup folders ----------------
os.makedirs("temps/images", exist_ok=True)
os.makedirs("temps/logs", exist_ok=True)

# ---------------- Helper functions ----------------
def parse_bool(value):
    """Parse boolean from string or int"""
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes')
    return bool(int(value))


def generate_image(prompt, run_id, rep_id, step_id, temp=0.7, saveAll=True, gen_idx=0, interp_idx=0, is_sdxl=True):
    if is_sdxl:
        prompt_embeds, _, pooled_prompt_embeds, _ = pipe.encode_prompt(prompt)
        prompt_embeds_2, _, pooled_prompt_embeds_2, _ = pipe.encode_prompt("")  # Empty prompt disables CLIP conditioning

        # Run SDXL with embedding inputs (no string prompts)
        image = pipe(
            prompt_embeds=prompt_embeds,
            pooled_prompt_embeds=pooled_prompt_embeds,
            prompt_embeds_2=prompt_embeds_2,
            pooled_prompt_embeds_2=pooled_prompt_embeds_2,
            num_inference_steps=25
        ).images[0]
    else:
        # Regular SD 1.5 - simpler interface
        image = pipe(
            prompt=prompt,
            num_inference_steps=25
        ).images[0]

    # Always save as 512x512
    #image = image.resize((512, 512), Image.LANCZOS)
    image = image.resize((256, 256), Image.LANCZOS)
    # Save image with structured filename
    if saveAll:
        fname = f"temps/images/run_{run_id:03}_rep_{rep_id}_step_{step_id:03}_temp_{temp}_gen_{gen_idx}_interp_{interp_idx}.png"
    else:
        fname = f"temps/images/run_{run_id:03}_rep_{rep_id}_step_LAST_temp_{temp}_gen_{gen_idx}_interp_{interp_idx}.png"
    image.save(fname, optimize=True)
    return fname


def describe_image(image_path, temp=0.7, interpreter_model="llava"):
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
    prompt = (
        "Describe this image in vivid, artistic terms. "
        "The description must be 50 words or fewer. "
        "Do not exceed the limit. Return only the description. Do not explain."
    )
    response = ollama.generate(
        model=interpreter_model,
        prompt=prompt,
        images=[img_b64],
        options={"temperature": temp}
    )
    return response["response"].strip()


# ---------------- Main ----------------
if len(sys.argv) < 7:
    print("Usage: python script.py <run_id> <temp> <saveAll> <port> <gen_idx> <interp_idx>")
    sys.exit(1)

run_id = int(sys.argv[1])
temp = float(sys.argv[2])
saveAll = parse_bool(sys.argv[3])
thePort = int(sys.argv[4])
gen_idx = int(sys.argv[5])
interp_idx = int(sys.argv[6])

# Validate indices
if not (0 <= gen_idx < len(GENERATORS)):
    print(f"Error: gen_idx must be 0-{len(GENERATORS)-1}")
    sys.exit(1)
if not (0 <= interp_idx < len(INTERPRETERS)):
    print(f"Error: interp_idx must be 0-{len(INTERPRETERS)-1}")
    sys.exit(1)

generator_model = GENERATORS[gen_idx]
interpreter_model = INTERPRETERS[interp_idx]
is_sdxl = USES_SDXL[gen_idx]

os.environ["OLLAMA_HOST"] = f"http://127.0.0.1:{thePort}"

print(f"Run {run_id}, temp={temp}, port={thePort}")
print(f"Generator: {generator_model} (index {gen_idx})")
print(f"Interpreter: {interpreter_model} (index {interp_idx})")
print(f"Pipeline type: {'SDXL' if is_sdxl else 'SD 1.5'}")

# ---------------- Stable Diffusion setup ----------------
if is_sdxl:
    pipe = StableDiffusionXLPipeline.from_pretrained(
        generator_model,
        torch_dtype=torch.float16,
        variant="fp16"
    ).to("cuda")
else:
    pipe = StableDiffusionPipeline.from_pretrained(
        generator_model,
        torch_dtype=torch.float16
    ).to("cuda")

# ---------------- Load reservoir ----------------
reservoir = pickle.load(open("reservoir_100.pkl", "rb"))

num_repeats = 1
steps_per_run = 100

initial_prompt = reservoir[run_id]

for rep_id in range(num_repeats):
    log_path = f"temps/logs/run_{run_id:03}_rep_{rep_id}_temp_{temp}_gen_{gen_idx}_interp_{interp_idx}.csv"
    prompts_this_run = []
    start_step = 0
    prompt = initial_prompt

    # ---------- Resume logic ----------
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                reader = list(csv.reader(f))
                if len(reader) > 1:
                    header = reader[0]
                    rows = reader[1:]
                    # parse last valid row
                    last_row = rows[-1]
                    last_step = int(last_row[2])
                    prompt = last_row[3]  # last generated prompt becomes new seed
                    start_step = last_step + 1
                    prompts_this_run = rows  # keep what we already have
                    print(f"↩ Resuming from step {start_step} (last prompt restored).")
        except Exception as e:
            print(f"⚠️ Could not read existing log ({e}); restarting from scratch.")

    # ---------- Skip finished runs ----------
    if start_step >= steps_per_run:
        print(f"✓ Run {run_id} rep {rep_id} already complete. Skipping.")
        continue

    print(f"▶ Run {run_id}, Repeat {rep_id}, Temp {temp}, starting at step {start_step}...")

    # ---------- Main loop ----------
    for step_id in range(start_step, steps_per_run):
        img_path = generate_image(prompt, run_id, rep_id, step_id, temp, saveAll, gen_idx, interp_idx, is_sdxl)
        new_prompt = describe_image(img_path, temp, interpreter_model)
        prompts_this_run.append((run_id, rep_id, step_id, prompt))
        prompt = new_prompt

        # Save progress after each step (safe mid-run resume point)
        with open(log_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["run_id", "rep_id", "step", "prompt"])
            writer.writerows(prompts_this_run)

        print(f"✓ Step {step_id}/{steps_per_run-1} done.")

    print(f"✓ Finished run {run_id}, rep={rep_id}, temp={temp}, gen={gen_idx}, interp={interp_idx}")