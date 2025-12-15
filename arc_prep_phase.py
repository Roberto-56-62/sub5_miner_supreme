# ============================================================
# ARC PREP PHASE – Hone compliant (NO git, NO download)
# ============================================================

import os

SOLVER_DIR = os.environ.get("SOLVER_DIR", "/app/arc_solver")


def run_prep():
    print("[PREP] Starting prep phase (Hone compliant)")
    print(f"[PREP] Expected solver dir: {SOLVER_DIR}")

    # --------------------------------------------------
    # CHECK: solver deve essere già presente nel repo
    # --------------------------------------------------
    if not os.path.isdir(SOLVER_DIR):
        raise RuntimeError(
            f"[PREP] Solver directory not found: {SOLVER_DIR}\n"
            f"[PREP] The solver must be bundled inside the miner repository."
        )

    print("[PREP] Solver directory found.")
    print("[PREP] Prep phase completed successfully.")


if __name__ == "__main__":
    run_prep()

