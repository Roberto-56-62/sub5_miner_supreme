# ============================================================
# ARC PREP PHASE – SUPREME_V2 (Subnet 5)
# ============================================================

import os
from transformers import AutoTokenizer, AutoModelForCausalLM

HF_REPO = "bobroller125/Supreme_V2"
MODEL_DIR = "/app/models/Supreme_V2"


def run_prep():
    print("[PREP] 🔵 Avvio fase PREP")
    print(f"[PREP] 📦 Repo HF: {HF_REPO}")
    print(f"[PREP] 📁 Destinazione: {MODEL_DIR}")

    # Se il modello è già presente, NON riscarichiamo
    if os.path.isdir(MODEL_DIR) and os.path.isfile(os.path.join(MODEL_DIR, "config.json")):
        print("[PREP] ✅ Modello già presente, skip download")
        return

    os.makedirs(MODEL_DIR, exist_ok=True)

    print("[PREP] ⬇️ Download tokenizer (public HF)")
    AutoTokenizer.from_pretrained(
        HF_REPO,
        use_fast=False,
        cache_dir=MODEL_DIR,
    )

    print("[PREP] ⬇️ Download modello (public HF)")
    AutoModelForCausalLM.from_pretrained(
        HF_REPO,
        cache_dir=MODEL_DIR,
    )

    print("[PREP] ✅ Supreme_V2 scaricato correttamente")

