import json
from utilities.logger import log
from utilities.json_utils import normalize_json


def run_prep_phase(task_json):
    log("🧩 Prep Phase: parsing JSON...", "cyan")

    try:
        data = json.loads(task_json)
    except Exception as e:
        log(f"❌ Errore JSON: {e}", "red")
        return {"error": "invalid_json"}

    normalized = normalize_json(data)
    return normalized

