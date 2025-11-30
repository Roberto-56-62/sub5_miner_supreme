import torch
from utilities.logger import log
from utilities.prompt_tools import build_prompt
from utilities.model_optimizer import prewarm_model


def run_inference_phase(model, tokenizer, prep_data):
    log("🧠 Inference Phase...", "cyan")

    prewarm_model(model)

    prompt = build_prompt(prep_data)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.2,
            top_p=0.95,
            do_sample=False
        )

    return tokenizer.decode(output[0], skip_special_tokens=True).strip()

