# ============================================================
# ARC INFERENCE PHASE – STUB (Subnet 5 / Hone)
# ============================================================

import json
import os
import subprocess

# Path standard Hone
DATASET_DIR = "/app/data"
OUTPUT_DIR = "/app/output"


def _load_dataset():
    """
    Hone monta il dataset in /app/data
    Il nome file può variare → li cerchiamo in modo robusto
    """
    candidates = [
        "dataset.json",
        "tasks.json",
        "miner_current_dataset.json",
    ]

    for name in candidates:
        path = os.path.join(DATASET_DIR, name)
        if os.path.exists(path):
            with open(path, "r") as f:
                return path, json.load(f)

    raise RuntimeError("Dataset Hone non trovato in /app/data")


def run_inference():
    print("[INFERENCE] 🔵 Avvio inference phase")

    # --------------------------------------------------------
    # LOAD DATASET
    # --------------------------------------------------------
    dataset_path, dataset = _load_dataset()
    print(f"[INFERENCE] Dataset caricato da: {dataset_path}")
    print(f"[INFERENCE] Numero task: {len(dataset)}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "results.json")

    # --------------------------------------------------------
    # CHIAMATA AL SOLVER ESTERNO (NON-MODELLO)
    # (per ora DISATTIVATA)
    # --------------------------------------------------------
    # ESEMPIO FUTURO:
    # subprocess.run(
    #     ["python3", "solver_main.py", dataset_path, output_file],
    #     check=True,
    # )

    # --------------------------------------------------------
    # OUTPUT VALIDO (TEST B)
    # --------------------------------------------------------
    result = {
        "phase": "inference",
        "status": "success",
        "predictions": [],
        "meta": {
            "solver": "stub",
            "tasks_seen": len(dataset)
        }
    }

    with open(output_file, "w") as f:
        json.dump(result, f)

    print(f"[INFERENCE] ✅ Output scritto in {output_file}")
    print("[INFERENCE] ✅ Inference completata con successo")

