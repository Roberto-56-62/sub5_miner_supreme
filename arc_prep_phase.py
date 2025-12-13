# =============================================================
# ARC PREP PHASE – SUBNET 5 (ARC-AGI-2)
# =============================================================
# Internet: ABILITATO
# Obiettivo:
#   - Scaricare modello + tokenizer Supreme_V2
#   - GENERARE tokenizer.json
#   - Salvare tutto localmente per inference OFFLINE
# =============================================================

import os
import json
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "bobroller125/supreme_v2"
MODEL_DIR = os.environ.get("SUPREME_V2_DIR", "/app/models/Supreme_V2")


def ensure_dir(path: str):
    if path:
        os.makedirs(path, exist_ok=True)


def write_json(obj, path: str):
    ensure_dir(os.path.dirname(path))
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)


def run_prep(input_dir: str, output_dir: str) -> None:
    print("[PREP] 🔵 Avvio PREP PHASE – Supreme_V2")
    print(f"[PREP] 🔵 Repo HF: {MODEL_ID}")
    print(f"[PREP] 🔵 Target dir: {MODEL_DIR}")

    ensure_dir(MODEL_DIR)

    start = time.time()

    # =========================================================
    # 1. TOKENIZER (CRITICO)
    # =========================================================
    print("[PREP] 🔵 Download + build tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    tokenizer.save_pretrained(MODEL_DIR)
    print("[PREP] 🟢 tokenizer.json generato")

    # =========================================================
    # 2. MODELLO
    # =========================================================
    print("[PREP] 🔵 Download modello...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    )
    model.save_pretrained(MODEL_DIR)
    print("[PREP] 🟢 modello salvato")

    elapsed = time.time() - start
    print(f"[PREP] 🟢 Download completato in {elapsed:.2f}s")

    # =========================================================
    # 3. STATUS
    # =========================================================
    ensure_dir(output_dir)

    status = {
        "phase": "prep",
        "status": "success",
        "model_id": MODEL_ID,
        "model_path": MODEL_DIR,
        "tokenizer_files": os.listdir(MODEL_DIR),
    }

    write_json(status, os.path.join(output_dir, "prep_status.json"))

    print("[PREP] 🎉 PREP PHASE COMPLETATA")

