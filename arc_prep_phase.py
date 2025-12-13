# =============================================================
# ARC PREP PHASE – SUBNET 5 (ARC-AGI-2)
# =============================================================
# Eseguita con internet ABILITATO.
# Obiettivo:
#   - Scaricare modello + tokenizer Supreme_V2 da HuggingFace
#   - Salvare TUTTO localmente in /app/models/Supreme_V2
#   - Garantire che inference possa girare OFFLINE
# =============================================================

import os
import json
import time
from huggingface_hub import snapshot_download

# ⚠️ Repo HF CORRETTO (case-sensitive)
MODEL_NAME = "bobroller125/supreme_v2"

# Directory locale dei modelli
MODEL_DIR = os.environ.get("SUPREME_V2_DIR", "/app/models/Supreme_V2")


# -------------------------- Utility --------------------------

def ensure_dir(path: str) -> None:
    if path:
        os.makedirs(path, exist_ok=True)


def safe_write_json(obj, path: str) -> None:
    try:
        ensure_dir(os.path.dirname(path))
        with open(path, "w") as f:
            json.dump(obj, f, indent=2)
    except Exception as e:
        print(f"[PREP] 🔴 Errore scrittura JSON {path}: {e}")


def assert_required_files(model_dir: str) -> None:
    """
    Verifica che i file MINIMI richiesti da transformers
    siano presenti per inference offline.
    """
    required_files = [
        "config.json",
        "generation_config.json",
        "tokenizer_config.json",
        "special_tokens_map.json",
    ]

    missing = []
    for fname in required_files:
        if not os.path.exists(os.path.join(model_dir, fname)):
            missing.append(fname)

    if missing:
        raise RuntimeError(
            f"[PREP] ❌ File mancanti in {model_dir}: {missing}"
        )


# -------------------------- Prep Phase --------------------------

def run_prep(input_dir: str, output_dir: str) -> None:
    print("[PREP] 🔵 Avvio PREP PHASE – Supreme_V2")
    print(f"[PREP] 🔵 Repo HF: {MODEL_NAME}")
    print(f"[PREP] 🔵 Target dir: {MODEL_DIR}")

    ensure_dir("/app/models")
    ensure_dir(MODEL_DIR)

    # =============================================================
    # 1. Download snapshot completo (MODEL + TOKENIZER)
    # =============================================================
    start_time = time.time()

    snapshot_download(
        repo_id=MODEL_NAME,
        local_dir=MODEL_DIR,
        local_dir_use_symlinks=False,
        resume_download=True,
    )

    elapsed = time.time() - start_time
    print(f"[PREP] 🟢 Download completato in {elapsed:.2f}s")

    # =============================================================
    # 2. Verifica integrità minima (CRITICO)
    # =============================================================
    print("[PREP] 🔵 Verifica file richiesti per inference offline...")
    assert_required_files(MODEL_DIR)
    print("[PREP] 🟢 Verifica OK")

    # =============================================================
    # 3. Scrittura stato prep
    # =============================================================
    ensure_dir(output_dir)

    status = {
        "phase": "prep",
        "status": "success",
        "model_name": MODEL_NAME,
        "model_path": MODEL_DIR,
    }

    status_file = os.path.join(output_dir, "prep_status.json")
    safe_write_json(status, status_file)

    print(f"[PREP] 🟢 prep_status.json scritto in {status_file}")
    print("[PREP] 🎉 PREP PHASE COMPLETATA CON SUCCESSO")

