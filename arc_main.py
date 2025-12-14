# ============================================================
# ARC MAIN – SUPREME_V2 (Subnet 5 / Hone)
# ============================================================

import argparse
from arc_prep_phase import run_prep
from arc_inference_phase import run_inference


def main():
    parser = argparse.ArgumentParser(description="ARC Solver Entry Point")
    parser.add_argument("--phase", required=True, choices=["prep", "inference"])
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    print(f"[MAIN] 🚀 ARC pipeline – phase={args.phase}")

    if args.phase == "prep":
        run_prep()
    elif args.phase == "inference":
        run_inference(args.input, args.output)

    print("[MAIN] ✅ Phase completata")


if __name__ == "__main__":
    main()

