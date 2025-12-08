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
    """
    Converte una griglia ARC 2D (interi 0-9) in un formato testo leggibile
    per il modello Supreme_V2.
    Esempio:
      [[1,2,3],[4,5,6]] → "1 2 3 | 4 5 6"
    """
    return " | ".join(" ".join(str(c) for c in row) for row in grid)


def _try_parse_json_grid(text: str) -> List[List[int]] | None:
    """
    Tenta di interpretare la risposta come JSON di tipo [[int, ...], ...].
    Se non riesce, restituisce None.
    """
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
    """
    Converte una risposta del modello in una griglia 2D.
    La Sub5 richiede output rigorosamente in forma 2D di interi.

    Formati accettati, ad esempio:
      - "1 2 3 | 4 5 6"
      - "[[1,2,3],[4,5,6]]"
    """
    # Normalizza testo
    text = (text or "").strip()

    # 1) Tentativo JSON (es: "[[1,2],[3,4]]")
    json_grid = _try_parse_json_grid(text)
    if json_grid is not None:
        if not json_grid:
            return [[0]]
        return json_grid

    # 2) Parsing semplice tipo "1 2 3 | 4 5 6"
    try:
        # Togli newline, sostituisci virgole con spazi
        clean = text.replace("\n", " ").replace(",", " ")
        # Split righe usando '|'
        rows = [r for r in clean.split("|") if r.strip()]

        grid: List[List[int]] = []
        for row in rows:
            tokens = row.strip().split()
            nums = []
            for t in tokens:
                if t.isdigit():
                    # Limita a cifre 0-9 come richiesto da ARC classico
                    val = int(t)
                    if 0 <= val <= 9:
                        nums.append(val)
            if nums:
                grid.append(nums)

        # Se non siamo riusciti a estrarre nulla → fallback
        if not grid:
            return [[0]]

        return grid

    except Exception:
        # fallback → grid minima; il validator la considera errore parziale
        return [[0]]


def _sanitize_grid(grid: List[List[int]]) -> List[List[int]]:
    """
    Garantisce che il risultato sia una griglia 2D non vuota.
    """
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
        """
        Carica Supreme_V2 dai pesi salvati nella prep phase.

        Parameters
        ----------
        use_vllm : bool
            Placeholder per future estensioni (non usato al momento).
        """
        self.use_vllm = use_vllm

        print("[ARC_SOLVER] 🔵 Inizializzazione ARCSolver (Supreme_V2)...")
        print(f"[ARC_SOLVER] 🔵 MODEL_DIR: {MODEL_DIR}")

        start_load = time.time()

        # Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)

        # Modello: preferisci CUDA se disponibile, altrimenti CPU.
        if torch.cuda.is_available():
            print("[ARC_SOLVER] 🔵 CUDA disponibile → uso GPU (float16)")
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_DIR,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                device_map="auto",  # lascia gestire il device a HF/accelerate
            )
        else:
            print("[ARC_SOLVER] 🟡 CUDA non disponibile → uso CPU")
            self.model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)
            self.model.to("cpu")

        self.model.eval()

        # Modalità deterministica
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
        """
        train_examples: lista di dict ARC:
          [
            {"input": grid, "output": grid},
            ...
          ]
        test_input: grid 2D → da trasformare in output

        Return: grid 2D con predizione (lista di liste di int)
        """
        start_time = time.time()

        try:
            # ============================================================
            # 1. Costruzione prompt testuale per Supreme_V2
            # ============================================================
            prompt_lines = ["Solve the ARC task.\n"]

            for idx, ex in enumerate(train_examples):
                inp_grid = ex.get("input")
                out_grid = ex.get("output")

                if inp_grid is None or out_grid is None:
                    continue

                inp = grid_to_text(inp_grid)
                out = grid_to_text(out_grid)

                prompt_lines.append(f"Example {idx + 1}:")
                prompt_lines.append(f"Input: {inp}")
                prompt_lines.append(f"Output: {out}")
                prompt_lines.append("")  # riga vuota

            prompt_lines.append(f"Test Input: {grid_to_text(test_input)}")
            prompt_lines.append("Predicted Output:")

            prompt = "\n".join(prompt_lines)

            # ============================================================
            # 2. Generazione del modello
            # ============================================================
            inputs = self.tokenizer(prompt, return_tensors="pt")
            inputs = inputs.to(self.model.device)

            with torch.no_grad():
                output_ids = self.model.generate(
                    **inputs,
                    max_new_tokens=200,
                    temperature=0.0,     # deterministico
                    do_sample=False,      # NO sampling
                    pad_token_id=self.tokenizer.eos_token_id,
                )

            decoded = self.tokenizer.decode(
                output_ids[0],
                skip_special_tokens=True,
            )

            # ============================================================
            # 3. Estrarre SOLO la parte dopo “Predicted Output:”
            # ============================================================
            if "Predicted Output:" in decoded:
                decoded = decoded.split("Predicted Output:", 1)[1]

            # ============================================================
            # 4. Convertire risultato → griglia ARC
            # ============================================================
            raw_grid = text_to_grid(decoded)
            grid = _sanitize_grid(raw_grid)

            elapsed = time.time() - start_time
            print(f"[ARC_SOLVER] 🟢 Predizione ottenuta in {elapsed:.2f}s: {grid}")

            return grid

        except Exception as e:
            elapsed = time.time() - start_time
            print(f"[ARC_SOLVER] 🔴 ERRORE durante solve() dopo {elapsed:.2f}s: {e}")
            # fallback garantito → evita crash del Sandbox Runner / validator
            return [[0]]

