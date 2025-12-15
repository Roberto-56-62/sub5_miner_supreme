# ============================================================
# ARC INFERENCE PHASE – STUB (Subnet 5 / Hone)
# ============================================================

import json
import os

SEARCH_ROOTS = [
    "/input",        # <-- QUESTO È QUELLO GIUSTO
    "/app/data",     # fallback
]

OUTPUT_DIR = "/app/output"


def _find_dataset_file():
    """
    Hone runner monta il dataset nel container sotto /input.
    Facciamo scan robusta multi-root.
    """
    for base in SEARCH_ROOTS:
        if not os.path.exists(base):
            continue

        for root, _, files in os.walk(base):
            for name in files:
                lname = name.lower()
                if lname.endswith(".json") and (
                    "dataset" in lname
                    or "task" in lname
                    or "tasks" in lname
                ):
                    return os.path.join(root, name)

    raise RuntimeError(
        f"Dataset Hone non trovato. Scan effettuata in: {SEARCH_ROOTS}"
    )


def run_inference():
    print("[INFERENCE] 🔵 Avvio inference phase")
    print(f"[INFERENCE] Scan roots: {SEARCH_ROOTS}")

    dataset_path = _find_dataset_file()
    print(f"[INFERENCE] ✅ Dataset trovato: {dataset_path}")

    with open(dataset_path, "r") as f:
        dataset = json.load(f)

    print(f"[INFERENCE] Numero task caricati: {len(dataset)}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "results.json")

    # --------------------------------------------------------
    # QUI IN FUTURO: NON-MODEL SOLVER
    # --------------------------------------------------------

    result = {
        "phase": "inference",
        "status": "success",
        "predictions": [],
        "meta": {
            "solver": "stub",
            "tasks_seen": len(dataset),
        },
    }

    with open(output_file, "w") as f:
        json.dump(result, f)

    print(f"[INFERENCE] ✅ Output scritto in {output_file}")
    print("[INFERENCE] ✅ Inference completata con successo")

