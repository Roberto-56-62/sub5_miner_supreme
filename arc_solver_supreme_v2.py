# ============================================================
# ARC SOLVER – SUPREME_V2 (Subnet 5 – ARC-AGI-2)
# ============================================================

import os
import time
import json
from typing import List, Dict, Any

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

# ============================================================
# CONFIG
# ============================================================

# 🔓 Modello PUBBLICO su HuggingFace
HF_MODEL_ID = "bobroller125/Supreme_V2"

# Cache HF (il runner monta /app/cache)
HF_CACHE_DIR = os.environ.get("TRANSFORMERS_CACHE", "/tmp/hf_cache")


# ============================================================
# Utils
# ============================================================

def grid_to_text(grid: List[List[int]]) -> str:
    return " | ".join(" ".join(str(c) for c in row) for row in grid)


def text_to_grid(text: str) -> List[List[int]]:
    text = (text or "").strip()

    try:
        obj = json.loads(text)
        if isinstance(obj, list):
            return [[int(x) for x in row] for row in obj if isinstance(row, list)]
    except Exception:
        pass

    rows = [r for r in text.replace(",", " ").split("|") if r.strip()]
    grid = []
    for r in rows:
        nums = [int(t) for t in r.split() if t.isdigit() and 0 <= int(t) <= 9]
        if nums:
            grid.append(nums)

    return grid if grid else [[0]]


# ============================================================
# Solver
# ============================================================

class ARCSolver:
    def __init__(self, use_vllm: bool = False) -> None:
        print("[ARC_SOLVER] 🔵 Inizializzazione ARCSolver (Supreme_V2)")
        print(f"[ARC_SOLVER] 🔵 HF_MODEL_ID: {HF_MODEL_ID}")
        print(f"[ARC_SOLVER] 🔵 CACHE_DIR: {HF_CACHE_DIR}")

        start = time.time()

        # =====================================================
        # TOKENIZER (slow, richiesto da Subnet 5)
        # =====================================================
        self.tokenizer = AutoTokenizer.from_pretrained(
            HF_MODEL_ID,
            use_fast=False,
            cache_dir=HF_CACHE_DIR,
        )

        # =====================================================
        # MODELLO
        # =====================================================
        if torch.cuda.is_available():
            self.model = AutoModelForCausalLM.from_pretrained(
                HF_MODEL_ID,
                torch_dtype=torch.float16,
                device_map="auto",
                low_cpu_mem_usage=True,
                cache_dir=HF_CACHE_DIR,
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                HF_MODEL_ID,
                cache_dir=HF_CACHE_DIR,
            ).to("cpu")

        self.model.eval()
        torch.manual_seed(0)

        print(f"[ARC_SOLVER] ✅ Supreme_V2 caricato in {time.time() - start:.2f}s")

    # =========================================================
    # Inference
    # =========================================================
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

            inputs = self.tokenizer(
                "\n".join(prompt),
                return_tensors="pt"
            ).to(self.model.device)

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

            return text_to_grid(decoded)

        except Exception as e:
            print(f"[ARC_SOLVER] 🔴 ERRORE solve(): {e}")
            return [[0]]

