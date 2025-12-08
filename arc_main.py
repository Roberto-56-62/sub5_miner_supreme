# =============================================================
# ARC MAIN – SUBNET 5 (ARC-AGI-2)
# =============================================================
# Il Sandbox Runner invoca questo file con:
#
#   python arc_main.py --phase prep --input /input --output /output
#   python arc_main.py --phase inference --input /input --output /output
#
# - PREP PHASE: internet ABILITATO → scarica Supreme_V2
# - INFERENCE PHASE: internet DISABILITATO → usa solver Supreme_V2
# =============================================================

import argparse
import sys
import os

from arc_prep_phase import run_prep
from arc_inference_phase import run_inference


# ----------------------------- MAIN -----------------------------

def main():
    parser = argparse.ArgumentParser(description="ARC-AGI-2 Solver – Subnet 5")

    parser.add_argument("--phase", type=str, required=True,
                        choices=["prep", "inference"],
                        help="Phase to run: prep or inference")

    parser.add_argument("--input", type=str, required=True,
                        help="Input directory containing task dataset")

    parser.add_argument("--output", type=str, required=True,
                        help="Output directory for results")

    args = parser.parse_args()

    phase = args.phase
    input_dir = args.input
    output_dir = args.output

    print(f"[MAIN] 🔵 Phase: {phase}")
    print(f"[MAIN] 🔵 Input directory: {input_dir}")
    print(f"[MAIN] 🔵 Output directory: {output_dir}")

    # =============================================================
    # Dispatch delle due fasi
    # =============================================================

    if phase == "prep":
        print("[MAIN] 🔧 Running PREP PHASE…")
        run_prep(input_dir, output_dir)
        print("[MAIN] 🟢 Prep phase completed.")
        return

    if phase == "inference":
        print("[MAIN] 🧠 Running INFERENCE PHASE…")
        run_inference(input_dir, output_dir)
        print("[MAIN] 🟢 Inference phase completed.")
        return

    # =============================================================
    # Se arriva qui, qualcosa è sbagliato (non dovrebbe accadere)
    # =============================================================
    print(f"[MAIN] 🔴 ERRORE: Phase non valida: {phase}")
    sys.exit(1)


# -------------------------- Entry Point --------------------------

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[MAIN] 🔴 CRASH FATALE: {e}")
        sys.exit(1)

