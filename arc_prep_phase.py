# ============================================================
# ARC PREP PHASE – SUPREME_V2
# Subnet 5 – ARC-AGI-2
# ============================================================

import os
from huggingface_hub import snapshot_download

# ============================================================
# CONFIG
# ============================================================

# Directory finale dove il modello DEVE esistere
MODEL_DIR = "/app/models/Supreme_V2"

# Repo Hugging Face del modello (TUO)
HF_REPO_ID = "Roberto-56-62/Supreme_V2"

# ============================================================
# PREP LOGIC
# ============================================================

def run_prep():
    print("[PREP] 🔵 Avvio fase PREP")

    # Assicura la directory /app/models
    os.makedirs("/app/models", exist_ok=True)

    # Se il modello è già presente → non riscaricare
    if os.path.exists(MODEL_DIR) and os.path.isdir(MODEL_DIR):
        print(f"[PREP] ✅ Modello già presente in {MODEL_DIR}")
        return

    # Download da Hugging Face (ONLINE)
    print(f"[PREP] ⬇️ Download Supreme_V2 da Hugging Face ({HF_REPO_ID})")

    snapshot_download(
        repo_id=HF_REPO_ID,
        local_dir=MODEL_DIR,
        local_dir_use_symlinks=False,
        resume_download=True
    )

    # Verifica finale
    if not os.path.exists(MODEL_DIR):
        raise RuntimeError("[PREP] ❌ Download fallito: MODEL_DIR non creato")

    print("[PREP] ✅ Download Supreme_V2 completato con successo")

