import time
import yaml

from utilities.logger import log
from utilities.hf_loader import load_model_and_tokenizer
from arc_prep_phase import run_prep_phase
from arc_inference_phase import run_inference_phase

# CONFIG
with open("config/miner_config.yaml", "r") as f:
    CFG = yaml.safe_load(f)


def main():
    log("🚀 Avvio Miner Subnet 5 – Supreme V2", "blue")

    hf_repo = CFG["model"]["hf_repo"]
    device = CFG["runtime"]["device"]

    log(f"📥 Carico modello HF: {hf_repo}", "yellow")
    model, tokenizer = load_model_and_tokenizer(hf_repo, device)

    while True:
        log("⏳ Attendo nuovo task ARC dal validator...", "cyan")
        task_json = input().strip()

        if task_json.lower() == "exit":
            log("🛑 Miner fermato.", "red")
            break

        t0 = time.time()

        prep_data = run_prep_phase(task_json)
        answer = run_inference_phase(model, tokenizer, prep_data)

        elapsed = time.time() - t0
        log(f"⏱ Tempo totale task: {elapsed:.3f}s", "green")

        print(answer)


if __name__ == "__main__":
    main()

