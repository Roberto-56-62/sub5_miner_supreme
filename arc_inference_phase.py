import json
from arc_solver.solver.core import ARCSolver

def run_inference(input_path="/input", output_path="/output"):
    with open(f"{input_path}/miner_current_dataset.json") as f:
        data = json.load(f)

    solver = ARCSolver()
    predictions = []

    for i, task in enumerate(data["tasks"]):
        pred = solver.solve(
            train_examples=task["train_examples"],
            test_input=task["test_input"],
        )
        predictions.append({
            "problem_index": i,
            "task_hash": task["task_hash"],
            "predicted_output": pred,
        })

    out = {
        "phase": "inference",
        "status": "success",
        "predictions": predictions,
    }

    with open(f"{output_path}/results.json", "w") as f:
        json.dump(out, f)

