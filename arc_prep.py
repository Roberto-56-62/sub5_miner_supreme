# import os
import sys
from huggingface_hub import snapshot_download

MODEL_REPO = "bobroller125/Supreme_V2"
MODEL_DIR = "/app/models/Supreme_V2"

def main():
    print("[PREP] 🔵 Download modello Supreme_V2")

    snapshot_download(
        repo_id=MODEL_REPO,
        local_dir=MODEL_DIR,
        local_dir_use_symlinks=False,
        allow_patterns=[
            "*.json",
            "*.safetensors",
            "*.bin",
            "*.model",
            "*.txt"
        ]
    )

    print("[PREP] 📂 Contenuto MODEL_DIR:")
    files_found = []
    for root, _, files in os.walk(MODEL_DIR):
        for f in files:
            path = os.path.join(root, f)
            files_found.append(path)
            print(" -", path)

    config_path = os.path.join(MODEL_DIR, "config.json")
    if not os.path.exists(config_path):
        print("❌ ERRORE FATALE: config.json NON TROVATO")
        print("❌ Questo NON è un modello Transformers valido")
        sys.exit(1)

    print("[PREP] ✅ config.json presente, modello valido")

if __name__ == "__main__":
    main()

