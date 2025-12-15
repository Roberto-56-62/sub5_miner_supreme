import os
import subprocess

SOLVER_REPO = os.environ.get("SOLVER_REPO", "https://github.com/TUO_USER/arc_solver")
SOLVER_BRANCH = os.environ.get("SOLVER_BRANCH", "main")
SOLVER_DIR = os.environ.get("SOLVER_DIR", "/app/arc_solver")

def run_prep():
    print("[PREP] Starting prep phase...")
    print(f"[PREP] SOLVER_REPO={SOLVER_REPO}")
    print(f"[PREP] SOLVER_BRANCH={SOLVER_BRANCH}")
    print(f"[PREP] SOLVER_DIR={SOLVER_DIR}")

    if os.path.exists(SOLVER_DIR) and os.path.isdir(SOLVER_DIR):
        print("[PREP] Solver dir already exists, skipping clone.")
        return

    subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", SOLVER_BRANCH, SOLVER_REPO, SOLVER_DIR],
        check=True,
    )
    print("[PREP] Solver cloned successfully.")

if __name__ == "__main__":
    run_prep()

