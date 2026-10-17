import torch
import torchvision
import diffusers
import transformers
import accelerate
import safetensors
import scipy
import numpy as np
from diffusers import StableDiffusionPipeline
import pickle
import os
import base64
import csv
from PIL import Image
from io import BytesIO
import ollama
import sys
from diffusers import StableDiffusionXLPipeline


def generate_image(prompt, run_id, rep_id, step_id,temp=0.7,saveAll=True):
    prompt_embeds, _, pooled_prompt_embeds, _ = pipe.encode_prompt(prompt)
    prompt_embeds_2, _, pooled_prompt_embeds_2, _ = pipe.encode_prompt("")  # Empty prompt disables CLIP conditioning

    # Run SDXL with *only* embedding inputs (no string prompts!)
    image = pipe(
        prompt_embeds=prompt_embeds,
        pooled_prompt_embeds=pooled_prompt_embeds,
        prompt_embeds_2=prompt_embeds_2,
        pooled_prompt_embeds_2=pooled_prompt_embeds_2,
        num_inference_steps=25
    ).images[0]
    # Resize to 256x256 for disk space reduction
    #image = image.resize((256, 256), Image.LANCZOS)
    # Resize to 512x512 for disk space reduction
    image = image.resize((512, 512), Image.LANCZOS)

    # Save image with structured filename
    if saveAll:
        fname = f"temps/images/run_{run_id:03}_rep_{rep_id}_step_{step_id:03}_temp_{temp}.png"
    else:
        fname = f"temps/images/run_{run_id:03}_rep_{rep_id}_step_LAST_temp_{temp}.png"
    image.save(fname, optimize=True)
    return fname


# Generate image from prompt    
#def generate_image(prompt, run_id, rep_id, step_id):
#    image = pipe(prompt, num_inference_steps=25).images[0]
#    image = image.resize((256, 256), Image.LANCZOS)  # high-quality downsampling
#    fname = f"trajectories/images/run_{run_id:03}_rep_{rep_id}_step_{step_id:03}.png"
#    image.save(fname, optimize=True)
#    return fname
    
# Describe image using LLaVA
def describe_image(image_path,temp=0.7):
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
    prompt = (
        "Describe this image in vivid, artistic terms. "
        "The description must be 50 words or fewer. "
        "Do not exceed the limit. Return only the description. Do not explain."
    )
    response = ollama.generate(
        model="llava",
        prompt=prompt,
        images=[img_b64],
        options={"temperature": temp}
    )
    return response["response"].strip()


# Set up folders
#os.makedirs("trajectories/images", exist_ok=True)
#os.makedirs("trajectories/logs", exist_ok=True)
os.makedirs("temps/images", exist_ok=True)
os.makedirs("temps/logs", exist_ok=True)

# Set up Stable Diffusion
#pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", safety_checker=None)
#pipe = pipe.to("cuda")

#pipe = StableDiffusionXLPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0")
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")
#pipe.to("cuda")

reservoir=pickle.load(open("reservoir_100.pkl","rb"))

# Loop through each prompt in reservoir
num_repeats = 1
steps_per_run = 100

run_id=param = int(sys.argv[1])
temp=float(sys.argv[2])
saveAll=bool(sys.argv[3])
thePort=int(sys.argv[4])

os.environ["OLLAMA_HOST"] = f"http://127.0.0.1:{thePort}"

print(run_id,temp,thePort)

initial_prompt=reservoir[run_id]
for rep_id in range(num_repeats):
    log_path = f"trajectories/logs/run_{run_id:03}_rep_{rep_id}_temp_{temp}.csv"
    
    # Skip if the file already exists and looks complete
    if os.path.exists(log_path):
        print(f"✓ Skipping run {run_id} rep {rep_id} _temp_{temp} (already exists)")
        continue

    prompt = initial_prompt
    prompts_this_run = []
    

    print(f"▶ Run {run_id}, Repeat {rep_id}, Temp {temp} starting...")

    for step_id in range(steps_per_run):
        img_path = generate_image(prompt, run_id, rep_id, step_id,temp,saveAll)
        new_prompt = describe_image(img_path,temp)
        prompts_this_run.append((run_id, rep_id, step_id, prompt))
        prompt = new_prompt

        # Save prompts log
        log_path = f"temps/logs/run_{run_id:03}_rep_{rep_id}_temp_{temp}.csv"
        with open(log_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["run_id", "rep_id", "step", "prompt"])
            writer.writerows(prompts_this_run)

    print(f"✓ Finished run {run_id}, rep {rep_id} {temp}")

    

