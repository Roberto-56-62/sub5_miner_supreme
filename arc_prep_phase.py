# ============================================================
# ARC PREP PHASE – SUPREME_V2 (Subnet 5)
# ============================================================

import os
from transformers import AutoTokenizer, AutoModelForCausalLM


HF_REPO = "Roberto-56-62/Supreme_V2"
MODEL_DIR = "/app/models/Supreme_V2"


def run_prep():
    print("[PREP] 🔵 Avvio fase PREP")
    print(f"[PREP] 📦 Repo HF: {HF_REPO}")
    print(f"[PREP] 📁 Destinazione: {MODEL_DIR}")

    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        raise RuntimeError(
            "[PREP] ❌ HF_TOKEN non presente. "
            "Impossibile scaricare modello privato."
        )

    os.makedirs(MODEL_DIR, exist_ok=True)

    print("[PREP] ⬇️ Download tokenizer da Hugging Face…")
    AutoTokenizer.from_pretrained(
        HF_REPO,
        token=hf_token,
        cache_dir=MODEL_DIR,
    )

    print("[PREP] ⬇️ Download modello da Hugging Face…")
    AutoModelForCausalLM.from_pretrained(
        HF_REPO,
        token=hf_token,
        cache_dir=MODEL_DIR,
    )

    print("[PREP] ✅ Supreme_V2 scaricato correttamente")

