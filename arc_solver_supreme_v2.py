# ============================================================
#  ARC SOLVER – SUPREME_V2 (Subnet 5 – ARC-AGI-2)
# ============================================================
# Questo file implementa il solver richiesto ufficialmente
# per la Subnet 5: un class-based solver con metodo `.solve()`
# compatibile con ARC-AGI-2 e con il Sandbox Runner.
#
# - Carica il modello Supreme_V2 (Mistral 7B adattato)
# - Genera output deterministico (no sampling)
# - Supporta fallback in caso di errore
# - Fa logging minimo (come richiesto dalla Sub5)
# ============================================================

import os
import time
import json
from typing import List, Dict, Any

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Directory dei pesi del modello.
# Deve essere coerente con arc_prep_phase.py:
#   MODEL_DIR = "/app/models/Supreme_V2"
MODEL_DIR = os.environ.get("SUPREME_V2_DIR", "/app/models/Supreme_V2")


# ------------------------------------------------------------
#  Utility → conversione griglia ARC (int) ↔ testo
# ------------------------------------------------------------
def grid_to_text(grid: List[List[int]]) -> str:
    return " | ".join(" ".join(str(c) for c in row) for row in grid)


def _try_parse_json_grid(text: str) -> List[List[int]] | None:
    try:
        obj = json.loads(text)
        if isinstance(obj, list) and obj:
            grid: List[List[int]] = []
            for row in obj:
                if not isinstance(row, list):
                    return None
                grid.append([int(x) for x in row])
            return grid
    except Exception:
        return None
    return None


def text_to_grid(text: str) -> List[List[int]]:
    text = (text or "").strip()

    json_grid = _try_parse_json_grid(text)
    if json_grid is not None:
        if not json_grid:
            return [[0]]
        return json_grid

    try:
        clean = text.replace("\n", " ").replace(",", " ")
        rows = [r for r in clean.split("|") if r.strip()]

        grid: List[List[int]] = []
        for row in rows:
            tokens = row.strip().split()
            nums = []
            for t in tokens:
                if t.isdigit():
                    val = int(t)
                    if 0 <= val <= 9:
                        nums.append(val)
            if nums:
                grid.append(nums)

        if not grid:
            return [[0]]

        return grid

    except Exception:
        return [[0]]


def _sanitize_grid(grid: List[List[int]]) -> List[List[int]]:
    if not grid or not isinstance(grid, list):
        return [[0]]

    cleaned: List[List[int]] = []
    for row in grid:
        if not isinstance(row, list):
            continue
        cleaned_row = [int(x) for x in row if isinstance(x, int)]
        if cleaned_row:
            cleaned.append(cleaned_row)

    if not cleaned:
        return [[0]]

    return cleaned


# ------------------------------------------------------------
#  Classe principale richiesta dalla Subnet 5
# ------------------------------------------------------------
class ARCSolver:
    def __init__(self, use_vllm: bool = False) -> None:
        self.use_vllm = use_vllm

        print("[ARC_SOLVER] 🔵 Inizializzazione ARCSolver (Supreme_V2)...")
        print(f"[ARC_SOLVER] 🔵 MODEL_DIR: {MODEL_DIR}")

        start_load = time.time()

        # 🔑 FIX SUBNET 5:
        # forza il caricamento SOLO da path locale
        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_DIR,
            local_files_only=True
        )

        if torch.cuda.is_available():
            print("[ARC_SOLVER] 🔵 CUDA disponibile → uso GPU (float16)")
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_DIR,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                device_map="auto",
                local_files_only=True
            )
        else:
            print("[ARC_SOLVER] 🟡 CUDA non disponibile → uso CPU")
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_DIR,
                local_files_only=True
            )
            self.model.to("cpu")

        self.model.eval()
        torch.manual_seed(0)

        load_time = time.time() - start_load
        print(f"[ARC_SOLVER] ✅ Supreme_V2 caricato in {load_time:.2f}s")

    # --------------------------------------------------------
    #  solve() → funzione OBBLIGATORIA per la Subnet 5
    # --------------------------------------------------------
    def solve(
        self,
        train_examples: List[Dict[str, Any]],
        test_input: List[List[int]],
    ) -> List[List[int]]:

        start_time = time.time()

        try:
            prompt_lines = ["Solve the ARC task.\n"]

            for idx, ex in enumerate(train_examples):
                inp_grid = ex.get("input")
                out_grid = ex.get("output")

                if inp_grid is None or out_grid is None:
                    continue

                prompt_lines.append(f"Example {idx + 1}:")
                prompt_lines.append(f"Input: {grid_to_text(inp_grid)}")
                prompt_lines.append(f"Output: {grid_to_text(out_grid)}")
                prompt_lines.append("")

            prompt_lines.append(f"Test Input: {grid_to_text(test_input)}")
            prompt_lines.append("Predicted Output:")

            prompt = "\n".join(prompt_lines)

            inputs = self.tokenizer(prompt, return_tensors="pt")
            inputs = inputs.to(self.model.device)

            with torch.no_grad():
                output_ids = self.model.generate(
                    **inputs,
                    max_new_tokens=200,
                    temperature=0.0,
                    do_sample=False,
                    pad_token_id=self.tokenizer.eos_token_id,
                )

            decoded = self.tokenizer.decode(
                output_ids[0],
                skip_special_tokens=True,
            )

            if "Predicted Output:" in decoded:
                decoded = decoded.split("Predicted Output:", 1)[1]

            raw_grid = text_to_grid(decoded)
            grid = _sanitize_grid(raw_grid)

            elapsed = time.time() - start_time
            print(f"[ARC_SOLVER] 🟢 Predizione ottenuta in {elapsed:.2f}s: {grid}")

            return grid

        except Exception as e:
            elapsed = time.time() - start_time
            print(f"[ARC_SOLVER] 🔴 ERRORE durante solve() dopo {elapsed:.2f}s: {e}")
            return [[0]]

