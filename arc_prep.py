# =============================================================
# ARC PREP PHASE – SUBNET 5 (ARC-AGI-2)
# =============================================================
# Questa fase viene eseguita con INTERNET ABILITATO dal runner.
#
# Scopo:
#   - Scaricare Supreme_V2 da HuggingFace
#   - Salvare il modello in /app/models/Supreme_V2
#   - Preparare l'ambiente per la fase di inference (offline)
#
# NOTE IMPORTANTI (Subnet 5):
#   - Nessuna inference qui
#   - Nessun caricamento del modello in RAM/GPU
#   - Solo download + verifica
# =============================================================

import os
import time
import json
from huggingface_hub import snapshot_download

# ===============================
# CONFIGURAZIONE MODELLO
# ===============================
MODEL_REPO = "bobroller125/Supreme_V2"
MODEL_DIR = os.environ.get("SUPREME_V2_DIR", "/app/models/Supreme_V2")

# ===============================
# UTILITY
# ===============================
def ensure_dir(path: str) -> None:
    if path:
        os.makedirs(path, exist_ok=True)


def write_status(output_dir: str, status: dict) -> None:
    ensure_dir(output_dir)
    path = os.path.join(output_dir, "prep_status.json")
    try:
        with open(path, "w") as f:
            json.dump(status, f, indent=2)
        print(f"[PREP] 🟢 prep_status.json scritto in {path}")
    except Exception as e:
        print(f"[PREP] 🔴 Errore scrittura prep_status.json: {e}")


# ===============================
# MAIN PREP FUNCTION
# ===============================
def run_prep(input_dir: str, output_dir: str) -> None:
    print("[PREP] 🔵 Avvio PREP PHASE (Subnet 5)")
    print(f"[PREP] 🔵 Repo modello: {MODEL_REPO}")
    print(f"[PREP] 🔵 Directory target: {MODEL_DIR}")

    ensure_dir("/app/models")
    ensure_dir(MODEL_DIR)

    start_time = time.time()

    try:
        print("[PREP] 🔵 Download Supreme_V2 in corso...")
        snapshot_download(
            repo_id=MODEL_REPO,
            local_dir=MODEL_DIR,
            local_dir_use_symlinks=False,
            resume_download=True,
        )

        elapsed = time.time() - start_time
        print(f"[PREP] 🟢 Download completato in {elapsed:.2f}s")

        status = {
            "phase": "prep",
            "status": "success",
            "model_repo": MODEL_REPO,
            "model_path": MODEL_DIR,
        }

    except Exception as e:
        print(f"[PRE]()

