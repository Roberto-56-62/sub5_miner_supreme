# ============================================================
# ARC MAIN – SUPREME_V2 (Subnet 5)
# ============================================================

from arc_prep_phase import run_prep
from arc_inference_phase import run_inference

def main():
    print("[MAIN] 🚀 Avvio pipeline ARC")

    # =========================
    # PREP PHASE (OBBLIGATORIA)
    # =========================
    print("[MAIN] 🧪 Esecuzione PREP phase")
    run_prep()

    # =========================
    # INFERENCE PHASE
    # =========================
    print("[MAIN] 🤖 Esecuzione INFERENCE phase")
    run_inference()

    print("[MAIN] ✅ Pipeline completata")

if __name__ == "__main__":
    main()

