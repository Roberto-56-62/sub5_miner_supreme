# ============================================================
# ARC INFERENCE PHASE – HONE-COMPATIBLE STUB (writable output)
# ============================================================

import json
import os


def _first_writable_dir(candidates):
    for d in candidates:
        try:
            os.makedirs(d, exist_ok=True)
            test_path = os.path.join(d, ".write_test")
            with open(test_path, "w") as f:
                f.write("ok")
            os.remove(test_path)
            return d
        except Exception:
            continue
    raise RuntimeError(f"Nessuna directory scrivibile tra: {candidates}")


def run_inference():
    print("[INFERENCE] 🔵 Avvio inference phase (Hone stub)")
    print("[INFERENCE] Nessun accesso diretto al dataset (by design)")

    # In Hone /app può essere read-only. Usiamo solo mount standard o /tmp.
    out_dir = _first_writable_dir(["/output", "/tmp/output"])
    output_file = os.path.join(out_dir, "results.json")

    result = {
        "phase": "inference",
        "status": "success",
        "predictions": [],
        "meta": {
            "solver": "stub",
            "note": "Hone ARC stub – no direct dataset access",
            "output_dir": out_dir,
        },
    }

    with open(output_file, "w") as f:
        json.dump(result, f)

    print(f"[INFERENCE] ✅ Output scritto in {output_file}")
    print("[INFERENCE] ✅ Inference completata con successo")

