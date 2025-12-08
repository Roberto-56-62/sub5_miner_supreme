# =============================================================
# ARC INFERENCE PHASE – SUBNET 5 (ARC-AGI-2)
# =============================================================
# Questo file viene eseguito dal Sandbox Runner con:
#
#   python arc_main.py --phase inference --input /input --output /output
#
# - INTERNET DISABILITATO
# - Il modello Supreme_V2 deve essere già disponibile in /app/models/Supreme_V2
# - L'output DEVE essere results.json con predictions per ogni task
# =============================================================

import json
import os
import time
from arc_solver_supreme_v2 import ARCSolver


# ------------------ Utility Sicure per i Validator ------------------

def safe_read_json(path):
    """Legge un file JSON evitando crash irrimediabili."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[INFERENCE] 🔴 ERRORE LETTURA JSON {path}: {e}")
        return None


def safe_write_json(obj, path):
    """Scrive un file JSON senza generare crash."""
    try:
        with open(path, "w") as f:
            json.dump(obj, f, indent=2)
        return True
    except Exception as e:
        print(f"[INFERENCE] 🔴 ERRORE SCRITTURA JSON {path}: {e}")
        return False


def ensure_output_dir(path):
    """Crea la directory output se non presente."""
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass


# ------------------ Inizializzazione solver UNA SOLA VOLTA ------------------

print("[INFERENCE] 🔵 Avvio fase INFERENCE…")
print("[INFERENCE] 🔵 Caricamento solver Supreme_V2…")

solver = ARCSolver()

print("[INFERENCE] 🟢 Solver Supreme_V2 pronto.")


# ------------------ Funzione Principale Richiesta dalla Subnet ------------------

def run_inference(input_dir, output_dir):
    """
    Esegue la fase di inference:
    - legge miner_current_dataset.json
    - risolve ogni task ARC
    - produce results.json nel formato richiesto
    """

    ensure_output_dir(output_dir)

    dataset_path = os.path.join(input_dir, "miner_current_dataset.json")

    print(f"[INFERENCE] 🔵 Carico dataset: {dataset_path}")

    dataset = safe_read_json(dataset_path)
    if dataset is None:
        print("[INFERENCE] 🔴 ERRORE: impossibile leggere il dataset.")
        return

    tasks = dataset.get("tasks", [])
    print(f"[INFERENCE] 🔵 Numero tasks nel dataset: {len(tasks)}")

    predictions = []

    # =============================================================
    # Loop sui problemi ARC
    # =============================================================
    for problem_index, task in enumerate(tasks):

        task_hash = task.get("task_hash", f"task_{problem_index}")
        train_examples = task.get("train_examples", None)
        test_input = task.get("test_input", None)

        print(f"[INFERENCE] 🧩 Task {problem_index} — {task_hash}")

        # Validazione minima
        if train_examples is None or test_input is None:
            print("[INFERENCE] 🔴 Task malformato → fallback [[0]]")
            predictions.append({
                "problem_index": problem_index,
                "task_hash": task_hash,
                "predicted_output": [[0]],
            })
            continue

        start_time = time.time()

        # ---------------------------------------------------------
        # Solve ARC task
        # ---------------------------------------------------------
        try:
            predicted_grid = solver.solve(train_examples, test_input)
        except Exception as e:
            print(f"[INFERENCE] 🔴 ERRORE solve(): {e}")
            predicted_grid = [[0]]  # fallback obbligatorio

        elapsed = time.time() - start_time

        print(f"[INFERENCE] 🟢 Task {problem_index} risolto in {elapsed:.2f}s — Output: {predicted_grid}")

        predictions.append({
            "problem_index": problem_index,
            "task_hash": task_hash,
            "predicted_output": predicted_grid
        })

    # =============================================================
    # Creazione results.json conforme alla Subnet 5
    # =============================================================
    results = {
        "phase": "inference",
        "status": "success",
        "predictions": predictions
    }

    output_path = os.path.join(output_dir, "results.json")

    if safe_write_json(results, output_path):
        print(f"[INFERENCE] 🟢 results.json salvato in: {output_path}")
    else:
        print(f"[INFERENCE] 🔴 ERRORE: impossibile salvare {output_path}")

    print("[INFERENCE] 🎉 INFERENCE COMPLETATA CON SUCCESSO")

