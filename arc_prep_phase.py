# ============================================================
# ARC PREP PHASE – SUPREME_V2 (Subnet 5 / Hone)
# ============================================================

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

HF_MODEL_ID = "bobroller125/Supreme_V2"
MODEL_DIR = "/app/models/Supreme_V2"


def run_prep():
    print("[PREP] 🔵 Avvio fase PREP (robust HF download)")
    print(f"[PREP] 📥 Modello: {HF_MODEL_ID}")

    # Directory writable per HuggingFace
    os.makedirs(MODEL_DIR, exist_ok=True)

    # ============================================================
    # Tokenizer (con resume e cache controllata)
    # ============================================================
    print("[PREP] 🔹 Download tokenizer…")
    tokenizer = AutoTokenizer.from_pretrained(
        HF_MODEL_ID,
        use_fast=False,
        cache_dir=MODEL_DIR,
        resume_download=True,
    )

    # ============================================================
    # Model (sharded, robust download)
    # ============================================================
    print("[PREP] 🔹 Download model shards…")
    model = AutoModelForCausalLM.from_pretrained(
        HF_MODEL_ID,
        cache_dir=MODEL_DIR,
        torch_dtype=torch.float16 if torch.cuda.is_available() else None,
        low_cpu_mem_usage=True,
        resume_download=True,
    )

    # ============================================================
    # Persistenza locale (per inference offline)
    # ============================================================
    tokenizer.save_pretrained(MODEL_DIR)
    model.save_pretrained(MODEL_DIR)

    print(f"[PREP] ✅ Download completato e modello salvato in {MODEL_DIR}")

