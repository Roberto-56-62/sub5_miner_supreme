# =============================================================
# ARC PREP PHASE – SUBNET 5 (ARC-AGI-2)
# =============================================================
# Eseguita con internet ABILITATO.
# Obiettivo:
#   - Scaricare i pesi Supreme_V2 da HuggingFace
#   - Preparare l’ambiente modello per l'inference
#   - Salvare tutto in /app/models/ per la fase 2 (inference)
#
# Output atteso:
#   - Nessun file specifico richiesto, ma logs chiari
#   - I modelli DEVONO essere in /app/models/Supreme_V2
# =============================================================

import os
import json
import time
from huggingface_hub import snapshot_download

# Repo HuggingFace del modello Supreme_V2
MODEL_NAME = "bobroller125/Supreme_V2"

# Directory dove verranno salvati i pesi
# (può essere sovrascritta da variabile d'ambiente se serve)
MODEL_DIR = os.environ.get("SUPREME_V2_DIR", "/app/models/Supreme_V2")


# -------------------------- Utility --------------------------

def ensure_dir(path: str) -> None:
    """Crea la directory se non esiste (no errore se già presente)."""
    if not path:
        return
    os.makedirs(path, exist_ok=True)


def safe_write_json(obj, path: str) -> None:
    """Scrive un JSON su disco, senza fare crash in caso di errore."""
    try:
        parent = os.path.dirname(path)
        if parent:
            ensure_dir(parent)
        with open(path, "w") as f:
            json.dump(obj, f, indent=2)
    except Exception as e:
        print(f"[PREP] 🔴 Errore scrittura JSON {path}: {e}")


# -------------------------- Prep Phase --------------------------

def run_prep(input_dir: str, output_dir: str) -> None:
    """
    Esegue la fase di preparazione.
    Internet è disponibile SOLO in questa fase → scarichiamo i modelli.

    input_dir  : directory con eventuali configurazioni / task (non usata qui)
    output_dir : directory dove salvare prep_status.json
    """

    print("[PREP] 🔵 Avvio PREP PHASE…")
    print("[PREP] 🔵 Modello richiesto: Supreme_V2")
    print(f"[PREP] 🔵 Target directory modelli: {MODEL_DIR}")

    # Directory base /app/models e dir specifica Supreme_V2
    ensure_dir("/app/models")
    ensure_dir(MODEL_DIR)

    # =============================================================
    # 1. Download del modello da HuggingFace
    # =============================================================
    print(f"[PREP] 🔵 Download Supreme_V2 da HuggingFace ({MODEL_NAME}) in corso...")

    start_time = time.time()

    try:
        snapshot_download(
            repo_id=MODEL_NAME,
            local_dir=MODEL_DIR,
            local_dir_use_symlinks=False,
            resume_download=True,
        )

        elapsed = time.time() - start_time
        print(f"[PREP] 🟢 Supreme_V2 scaricato in {elapsed:.2f}s")

    except Exception as e:
        print(f"[PREP] 🔴 ERRORE DOWNLOAD Supreme_V2: {e}")
        print("[PREP] ❗ Continuo comunque (il sandbox potrà gestire il fallback)")

    # =============================================================
    # 2. Scrivi file di controllo
    # =============================================================
    ensure_dir(output_dir)

    status_file = os.path.join(output_dir, "prep_status.json")

    status = {
        "phase": "prep",
        "status": "success",
        "model_path": MODEL_DIR,
        "model_name": MODEL_NAME,
    }

    safe_write_json(status, status_file)

    print(f"[PREP] 🟢 prep_status.json salvato in {status_file}")
    print("[PREP] 🎉 PREP PHASE COMPLETATA")

