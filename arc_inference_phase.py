# ============================================================
# ARC INFERENCE PHASE – STUB (Subnet 5 / Hone)
# ============================================================

import json
import os

DATA_ROOT = "/app/data"
OUTPUT_DIR = "/app/output"


def _find_dataset_file():
    """
    Hone salva il dataset in:
    /app/data/job_<id>/*.json

    Questa funzione lo individua in modo robusto.
    """
    for root, _, files in os.walk(DATA_ROOT):
        for name in files:
            if name.endswith(".json") and "dataset" in name.lower():
                return os.path.join(root, name)
            if name.endswith(".json") and "task" in name.lower():
                return os.path.join(root, name)

    raise RuntimeError("Dataset Hone non trovato (scan completa fallita)")


def run_inference():
    print("[INFERENCE] 🔵 Avvio inference phase")

    dataset_path = _find_dataset_file()
    print(f"[INFERENCE] Dataset trovato: {dataset_path}")

    with open(dataset_path, "r") as f:
        dataset = json.load(f)

    print(f"[INFERENCE] Numero task: {len(dataset)}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "results.json")

    # --------------------------------------------------------
    # QUI IN FUTURO: CHIAMATA AL NON-MODELLO
    # --------------------------------------------------------
    # for task in dataset:
    #     solve(task)

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

