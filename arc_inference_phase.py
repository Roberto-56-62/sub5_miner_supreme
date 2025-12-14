# ============================================================
# ARC INFERENCE PHASE – SUPREME_V2 (Subnet 5 / Hone)
# ============================================================

import json
import os
from arc_solver_supreme_v2 import ARCSolver


def run_inference(input_dir: str, output_dir: str):
    print("[INFERENCE] 🔵 Avvio fase INFERENCE")

    input_path = os.path.join(input_dir, "miner_current_dataset.json")
    output_path = os.path.join(output_dir, "results.json")

    with open(input_path, "r") as f:
        data = json.load(f)

    solver = ARCSolver()

    predictions = []

    for idx, task in enumerate(data.get("tasks", [])):
        result = solver.solve(
            train_examples=task["train_examples"],
            test_input=task["test_input"],
        )

        predictions.append(
            {
                "problem_index": idx,
                "task_hash": task.get("task_hash"),
                "predicted_output": result,
            }
        )

    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(
            {
                "phase": "inference",
                "status": "success",
                "predictions": predictions,
            },
            f,
            indent=2,
        )

    print(f"[INFERENCE] ✅ Results scritti in {output_path}")

