# ============================================================
#  ARC SOLVER – SUPREME_V2 (Subnet 5 – ARC-AGI-2)
# ============================================================

import os
import time
import json
from typing import List, Dict, Any

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_DIR = os.environ.get("SUPREME_V2_DIR", "/app/models/Supreme_V2")


def grid_to_text(grid: List[List[int]]) -> str:
    return " | ".join(" ".join(str(c) for c in row) for row in grid)


def _try_parse_json_grid(text: str):
    try:
        obj = json.loads(text)
        if isinstance(obj, list) and obj:
            return [[int(x) for x in row] for row in obj if isinstance(row, list)]
    except Exception:
        pass
    return None


def text_to_grid(text: str) -> List[List[int]]:
    text = (text or "").strip()

    json_grid = _try_parse_json_grid(text)
    if json_grid:
        return json_grid

    try:
        clean = text.replace("\n", " ").replace(",", " ")
        rows = [r for r in clean.split("|") if r.strip()]
        grid = []
        for row in rows:
            nums = [int(t) for t in row.split() if t.isdigit() and 0 <= int(t) <= 9]
            if nums:
                grid.append(nums)
        return grid if grid else [[0]]
    except Exception:
        return [[0]]


def _sanitize_grid(grid: List[List[int]]) -> List[List[int]]:
    return grid if grid and isinstance(grid, list) else [[0]]


class ARCSolver:
    def __init__(self, use_vllm: bool = False) -> None:
        self.use_vllm = use_vllm

        print("[ARC_SOLVER] 🔵 Inizializzazione ARCSolver (Supreme_V2)")
        print(f"[ARC_SOLVER] 🔵 MODEL_DIR: {MODEL_DIR}")

        start = time.time()

        # ✅ TOKENIZER: da HF repo (cache locale)
        self.tokenizer = AutoTokenizer.from_pretrained(
            "bobroller125/supreme_v2",
            local_files_only=True
        )

        # ✅ MODELLO: da path locale
        if torch.cuda.is_available():
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_DIR,
                torch_dtype=torch.float16,
                device_map="auto",
                low_cpu_mem_usage=True,
                local_files_only=True
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_DIR,
                local_files_only=True
            ).to("cpu")

        self.model.eval()
        torch.manual_seed(0)

        print(f"[ARC_SOLVER] ✅ Supreme_V2 caricato in {time.time() - start:.2f}s")

    def solve(
        self,
        train_examples: List[Dict[str, Any]],
        test_input: List[List[int]],
    ) -> List[List[int]]:

        try:
            prompt = ["Solve the ARC task.\n"]

            for i, ex in enumerate(train_examples):
                prompt.append(f"Example {i+1}:")
                prompt.append(f"Input: {grid_to_text(ex['input'])}")
                prompt.append(f"Output: {grid_to_text(ex['output'])}")
                prompt.append("")

            prompt.append(f"Test Input: {grid_to_text(test_input)}")
            prompt.append("Predicted Output:")

            inputs = self.tokenizer("\n".join(prompt), return_tensors="pt").to(self.model.device)

            with torch.no_grad():
                out = self.model.generate(
                    **inputs,
                    max_new_tokens=200,
                    temperature=0.0,
                    do_sample=False,
                    pad_token_id=self.tokenizer.eos_token_id,
                )

            decoded = self.tokenizer.decode(out[0], skip_special_tokens=True)
            if "Predicted Output:" in decoded:
                decoded = decoded.split("Predicted Output:", 1)[1]

            return _sanitize_grid(text_to_grid(decoded))

        except Exception as e:
            print(f"[ARC_SOLVER] 🔴 ERRORE solve(): {e}")
            return [[0]]

