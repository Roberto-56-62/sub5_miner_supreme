# =============================================================
# ARC UTILS – SUBNET 5 (ARC-AGI-2)
# =============================================================
# Utility comuni usate da prep_phase, inference_phase e solver.
#
# - Lettura/scrittura JSON sicura
# - Creazione directory
# - File helpers minimi
#
# NON usare librerie esterne: Subnet 5 richiede dipendenze minime.
# =============================================================

import os
import json


# ------------------------- Directory Utils -------------------------

def ensure_dir(path: str) -> None:
    """
    Crea una directory se non esiste, ignorando errori.
    """
    try:
        if path:
            os.makedirs(path, exist_ok=True)
    except Exception:
        pass


def ensure_parent_dir(file_path: str) -> None:
    """
    Garantisce che la directory padre di un file esista.
    """
    try:
        parent = os.path.dirname(file_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
    except Exception:
        pass


# ------------------------- JSON Utils -------------------------

def safe_read_json(path: str):
    """
    Legge un file JSON restituendo None in caso di errore.
    Non genera mai eccezioni non gestite.
    """
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[UTILS] 🔴 ERRORE LETTURA JSON {path}: {e}")
        return None


def safe_write_json(obj, path: str) -> bool:
    """
    Scrive un JSON su disco in modo sicuro.
    Restituisce True/False se l'operazione ha avuto successo.
    """
    try:
        ensure_parent_dir(path)
        with open(path, "w") as f:
            json.dump(obj, f, indent=2)
        return True
    except Exception as e:
        print(f"[UTILS] 🔴 ERRORE SCRITTURA JSON {path}: {e}")
        return False


# ------------------------- File Helpers -------------------------

def list_json_files(directory: str):
    """
    Restituisce una lista ordinata di file .json nella directory specificata.
    Usato dal runner o da test opzionali.
    """
    try:
        return sorted(
            f for f in os.listdir(directory)
            if f.lower().endswith(".json")
        )
    except Exception:
        return []

