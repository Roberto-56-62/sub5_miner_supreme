import numpy as np
from typing import Callable, List, Tuple, Dict

from .operators import (
    identity,
    rotate90,
    rotate180,
    rotate270,
    flip_h,
    flip_v,
    color_map,
)

from .region import find_bbox, crop, paste


class ARCSolver:
    def __init__(self):
        # --------------------------------------------------
        # OPERATORI GEOMETRICI (STEP 1–2–3)
        # --------------------------------------------------
        self.operators: List[Tuple[str, Callable]] = [
            ("identity", identity),
            ("rotate90", rotate90),
            ("rotate180", rotate180),
            ("rotate270", rotate270),
            ("flip_h", flip_h),
            ("flip_v", flip_v),
        ]

    # ==================================================
    # UTILS
    # ==================================================

    def _infer_color_mapping(
        self, src: np.ndarray, dst: np.ndarray
    ) -> Dict[int, int] | None:
        """
        Inferisce una mappatura colore → colore se esiste
        """
        mapping: Dict[int, int] = {}

        for s, d in zip(src.flatten(), dst.flatten()):
            if s == d:
                continue
            if s in mapping and mapping[s] != d:
                return None
            mapping[s] = d

        return mapping if mapping else None

    # ==================================================
    # SOLVER
    # ==================================================

    def solve(
        self,
        train_input,
        train_output,
        test_input,
    ) -> np.ndarray:
        """
        STEP 1 → operatori singoli
        STEP 3 → catene di 2 operatori
        STEP 4 → color mapping puro
        STEP 5 → geometria + color mapping
        STEP 6 → bounding box + ricorsione
        """

        # --------------------------------------------------
        # NORMALIZZAZIONE INPUT
        # --------------------------------------------------
        train_input = np.array(train_input)
        train_output = np.array(train_output)
        test_input = np.array(test_input)

        # --------------------------------------------------
        # STEP 1 – OPERATORI SINGOLI
        # --------------------------------------------------
        for name, op in self.operators:
            try:
                out = op(train_input)
                if out.shape == train_output.shape and np.array_equal(out, train_output):
                    print(f"[ARC] Solved with operator: {name}")
                    return op(test_input)
            except Exception:
                continue

        # --------------------------------------------------
        # STEP 3 – CATENE (DEPTH = 2)
        # --------------------------------------------------
        for name1, op1 in self.operators:
            for name2, op2 in self.operators:
                try:
                    out = op2(op1(train_input))
                    if out.shape == train_output.shape and np.array_equal(out, train_output):
                        print(f"[ARC] Solved with chain: {name1} → {name2}")
                        return op2(op1(test_input))
                except Exception:
                    continue

        # --------------------------------------------------
        # STEP 4 – COLOR MAPPING PURO
        # --------------------------------------------------
        mapping = self._infer_color_mapping(train_input, train_output)
        if mapping is not None:
            print(f"[ARC] Solved with color mapping: {mapping}")
            return color_map(test_input, mapping)

        # --------------------------------------------------
        # STEP 5 – GEOMETRIA + COLOR MAPPING
        # --------------------------------------------------
        for name, op in self.operators:
            try:
                geom_out = op(train_input)
                if geom_out.shape != train_output.shape:
                    continue

                mapping = self._infer_color_mapping(geom_out, train_output)
                if mapping is not None:
                    print(f"[ARC] Solved with {name} + color mapping: {mapping}")
                    return color_map(op(test_input), mapping)
            except Exception:
                continue

        # --------------------------------------------------
        # STEP 6 – BOUNDING BOX + RICORSIONE
        # --------------------------------------------------
        bbox = find_bbox(train_input, background=0)
        if bbox is not None:
            try:
                sub_train_in = crop(train_input, bbox)
                sub_train_out = crop(train_output, bbox)
                sub_test_in = crop(test_input, bbox)

                sub_result = self.solve(
                    sub_train_in,
                    sub_train_out,
                    sub_test_in,
                )

                print("[ARC] Solved with bounding box strategy")
                return paste(test_input, sub_result, bbox)
            except Exception:
                pass

        # --------------------------------------------------
        # FALLIMENTO
        # --------------------------------------------------
        raise RuntimeError("Nessuna regola ARC valida trovata")

