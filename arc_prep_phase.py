# ============================================================
# ARC PREP PHASE – SUPREME_V2 (Subnet 5 / Hone)
# ============================================================

import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

HF_MODEL_ID = "bobroller125/Supreme_V2"
MODEL_DIR = "/app/models/Supreme_V2"


def run_prep():
    print("[PREP] 🔵 Avvio fase PREP")
    print("[PREP] 📥 Download modello da HuggingFace")

    os.makedirs(MODEL_DIR, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(
        HF_MODEL_ID,
        use_fast=False,
        cache_dir=MODEL_DIR,
    )

    model = AutoModelForCausalLM.from_pretrained(
        HF_MODEL_ID,
        cache_dir=MODEL_DIR,
        torch_dtype=torch.float16 if torch.cuda.is_available() else None,
    )

    tokenizer.save_pretrained(MODEL_DIR)
    model.save_pretrained(MODEL_DIR)

    print(f"[PREP] ✅ Modello salvato in {MODEL_DIR}")

