# ============================================================
# ARC PREP PHASE – SUPREME_V2 (Subnet 5)
# ============================================================

import os
from transformers import AutoTokenizer, AutoModelForCausalLM

# =========================
# CONFIG
# =========================
HF_REPO_ID = "Roberto-56-62/Supreme_V2"   # <-- repo HF reale
MODEL_DIR = "/app/models/Supreme_V2"

# Cache HF SCRIVIBILE (IMPORTANTISSIMO)
os.environ["TRANSFORMERS_CACHE"] = "/app/cache/hf"
os.environ["HF_HOME"] = "/app/cache/hf"

def run_prep():
    print("[PREP] 🔵 Avvio fase PREP")
    print(f"[PREP] 📦 Repo HF: {HF_REPO_ID}")
    print(f"[PREP] 📁 Destinazione: {MODEL_DIR}")

    os.makedirs(MODEL_DIR, exist_ok=True)

    print("[PREP] ⬇️ Download tokenizer da Hugging Face…")
    AutoTokenizer.from_pretrained(
        HF_REPO_ID,
        cache_dir="/app/cache/hf"
    ).save_pretrained(MODEL_DIR)

    print("[PREP] ⬇️ Download model da Hugging Face…")
    AutoModelForCausalLM.from_pretrained(
        HF_REPO_ID,
        cache_dir="/app/cache/hf"
    ).save_pretrained(MODEL_DIR)

    print("[PREP] ✅ Supreme_V2 scaricato correttamente")

