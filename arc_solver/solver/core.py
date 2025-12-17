import numpy as np
from typing import Callable, List, Tuple, Dict, Optional

from .operators import (
    identity,
    rotate90,
    rotate180,
    rotate270,
    flip_h,
    flip_v,
    color_map,
)

from .region import (
    bbox_crop,
    find_bbox,
    crop,
    paste,
    translate_bbox,
)

# ============================================================
# UTILS GLOBALI
# ============================================================

def same_object_ignore_bg(
    a: np.ndarray,
    b: np.ndarray,
    background: int = 0,
) -> bool:
    if a.shape != b.shape:
        return False
    mask = (a != background) | (b != background)
    return np.array_equal(a[mask], b[mask])


# ============================================================
# ARC SOLVER
# ============================================================

class ARCSolver:
    def __init__(self):
        self.operators: List[Tuple[str, Callable]] = [
            ("identity", identity),
            ("rotate90", rotate90),
            ("rotate180", rotate180),
            ("rotate270", rotate270),
            ("flip_h", flip_h),
            ("flip_v", flip_v),
            ("bbox_crop", bbox_crop),
        ]

    # --------------------------------------------------
    # COLOR MAPPING (STRICT ARC)
    # --------------------------------------------------

    def _infer_color_mapping(
        self,
        src: np.ndarray,
        dst: np.ndarray,
        background: int,
    ) -> Optional[Dict[int, int]]:
        mapping: Dict[int, int] = {}

        for s, d in zip(src.flatten(), dst.flatten()):
            if s == d:
                continue

            # background NON PUÒ MAI essere coinvolto
            if s == background or d == background:
                return None

            if s in mapping and mapping[s] != d:
                return None

            mapping[s] = d

        return mapping if mapping else None

    # --------------------------------------------------
    # SOLVER
    # --------------------------------------------------

    def solve(self, train_input, train_output, test_input) -> np.ndarray:
        train_input = np.array(train_input)
        train_output = np.array(train_output)
        test_input = np.array(test_input)

        background = 0

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
                pass

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
                    pass

        # --------------------------------------------------
        # STEP 8 – TRANSLATION (PRIORITARIO)
        # --------------------------------------------------
        bbox_in = find_bbox(train_input, background)
        bbox_out = find_bbox(train_output, background)
        bbox_test = find_bbox(test_input, background)

        if bbox_in and bbox_out and bbox_test:
            patch_in = crop(train_input, bbox_in)
            patch_out = crop(train_output, bbox_out)
            patch_test = crop(test_input, bbox_test)

            if same_object_ignore_bg(patch_in, patch_out, background):
                dr = bbox_out[0] - bbox_in[0]
                dc = bbox_out[2] - bbox_in[2]

                new_bbox = translate_bbox(
                    bbox_test, dr, dc, test_input.shape
                )
                if new_bbox is not None:
                    out = np.full_like(test_input, background)
                    out = paste(out, patch_test, new_bbox, background)
                    print(f"[ARC] Solved with translation: dr={dr}, dc={dc}")
                    return out

        # --------------------------------------------------
        # STEP 6 – BOUNDING BOX + RICORSIONE
        # --------------------------------------------------
        if bbox_in is not None:
            sub_train_in = crop(train_input, bbox_in)
            sub_train_out = crop(train_output, bbox_in)
            sub_test_in = crop(test_input, bbox_in)

            try:
                sub_result = self.solve(
                    sub_train_in, sub_train_out, sub_test_in
                )
                print("[ARC] Solved with bounding box strategy")
                return paste(test_input, sub_result, bbox_in, background)
            except Exception:
                pass

        # --------------------------------------------------
        # STEP 4 – COLOR MAPPING PURO
        # CONSENTITO SOLO SE NON ESISTONO OGGETTI
        # --------------------------------------------------
        if not np.any(train_input != background):
            mapping = self._infer_color_mapping(
                train_input, train_output, background
            )
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

                mapping = self._infer_color_mapping(
                    geom_out, train_output, background
                )
                if mapping is not None:
                    print(f"[ARC] Solved with {name} + color mapping: {mapping}")
                    return color_map(op(test_input), mapping)
            except Exception:
                pass

        raise RuntimeError("Nessuna regola ARC valida trovata")


