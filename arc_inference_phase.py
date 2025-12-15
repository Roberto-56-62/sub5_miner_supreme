import json
import os
import sys
import numpy as np

SOLVER_DIR = os.environ.get("SOLVER_DIR", "/app/arc_solver")

# directory output: nel runner è scrivibile /output (come hai visto)
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "results.json")

def run_inference():
    print("[INFERENCE] Starting inference...")

    # assicura output scrivibile
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # aggiunge solver al path
    if SOLVER_DIR not in sys.path:
        sys.path.insert(0, SOLVER_DIR)

    try:
        from arc_solver.solver.core import ARCSolver
    except Exception as e:
        # fallback: output minimale ma non crashare il runner
        print(f"[INFERENCE] ERROR importing solver: {e}")
        with open(OUTPUT_FILE, "w") as f:
            json.dump({"predictions": [], "error": f"import_failed: {str(e)}"}, f)
        print(f"[INFERENCE] Wrote fallback output to {OUTPUT_FILE}")
        return

    solver = ARCSolver()

    # ⚠️ Qui per ora facciamo una demo “safe”: se non abbiamo dataset vero,
    # produciamo predictions vuote ma “formalmente ok”.
    # Nel punto C andiamo ad agganciare il dataset reale del runner.
    predictions = []

    with open(OUTPUT_FILE, "w") as f:
        json.dump({"predictions": predictions}, f)

    print(f"[INFERENCE] ✅ Wrote results to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_inference()

