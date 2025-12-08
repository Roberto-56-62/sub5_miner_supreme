Subnet 5 ARC Miner — Supreme_V2

This repository contains the official ARC-compliant miner implementation for Subnet 5 (HONE / Manifold Labs), using the Supreme_V2 model hosted on HuggingFace.

The miner follows the ARC-AGI-2 specification and implements both phases required by the Sandbox Runner:

PREP PHASE → Downloads and prepares the model

INFERENCE PHASE → Loads the model locally and solves ARC tasks

All components are deterministic and validator-safe.

📁 Project Structure
arc_main.py               → Central entrypoint (prep / inference)
arc_prep_phase.py         → Downloads Supreme_V2 from HuggingFace
arc_inference_phase.py    → Runs inference and produces results.json
arc_solver_supreme_v2.py  → ARC solver using the Supreme_V2 model
arc_utils.py              → Grid/text conversion helpers

config/
  └─ miner_config.yaml    → Model & inference configuration

Dockerfile                → Execution environment for validators
requirements.txt          → Python dependencies
tests/                    → Local testing utilities

⚙️ PREP PHASE

Executed by the Sandbox Runner with internet enabled:

python arc_main.py --phase prep --input /input --output /output


This phase:

Downloads model: bobroller125/supreme_v2

Saves it to: /app/models/Supreme_V2

Produces prep_status.json in /output

🧠 INFERENCE PHASE

Executed with internet disabled:

python arc_main.py --phase inference --input /input --output /output


This phase:

Loads the model from /app/models/Supreme_V2

Iterates over ARC tasks in miner_current_dataset.json

Uses ARCSolver.solve() to generate predictions

Outputs:

/output/results.json


In the exact specification required by Subnet 5.

🧩 Model

The miner uses the ARC-specialized:

Supreme_V2

Architecture: Mistral 7B (ARC fine-tuned)

Hosted at: bobroller125/supreme_v2

Loaded fully locally in inference phase (offline)

The solver is deterministic and includes fallback handling to ensure the miner never crashes.

🛠 Docker

The included Dockerfile builds the correct environment:

Python 3.10

Transformers / Torch GPU ready

Automatic entrypoint to arc_main.py

Validators build this container directly when scoring your miner.

✔️ Requirements

The miner uses:

transformers>=4.36.0
accelerate
huggingface_hub
torch
numpy
python-dotenv

💡 Notes

No internet access is allowed during inference.

Output is always guaranteed (failsafe grid returned on exceptions).

The project structure fully respects ARC-AGI-2 and Subnet 5 guidelines.

Designed for clean auditing and minimal external dependencies.

🎯 Status: Ready for Subnet 5 Validation

This repository contains a complete, fully functional ARC miner implementation for Subnet 5 using Supreme_V2 and is suitable for sandbox execution.
