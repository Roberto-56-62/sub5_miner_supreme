# ============================================================
# ARC INFERENCE PHASE – STUB (Subnet 5 / Hone)
# ============================================================

import json
import os
import subprocess


def run_inference(input_dir: str = "/input", output_dir: str = "/output"):
    """
    Inference stub.
    - Riceve input dal runner
    - Chiama il solver esterno (altro repository)
    - Scrive l'output per il validator
    """

    print("[INFERENCE] 🔵 Avvio inference stub")

    input_file = os.path.join(input_dir, "miner_current_dataset.json")
    output_file = os.path.join(output_dir, "results.json")

    if not os.path.exists(input_file):
        raise RuntimeError("Input dataset non trovato")

    os.makedirs(output_dir, exist_ok=True)

    # --------------------------------------------------------
    # CHIAMATA AL SOLVER ESTERNO
    # (qui verrà agganciato il non-modello)
    # --------------------------------------------------------
    # ESEMPIO:
    # subprocess.run(
    #     ["python3", "solver_main.py", input_file, output_file],
    #     check=True,
    # )

    # --------------------------------------------------------
    # TEMPORANEO: output vuoto valido (per test runner)
    # --------------------------------------------------------
    with open(output_file, "w") as f:
        json.dump(
            {
                "phase": "inference",
                "status": "success",
                "predictions": []
            },
            f
        )

    print("[INFERENCE] ✅ Inference stub completata")

