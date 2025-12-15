import numpy as np
from typing import Callable, List, Dict


# ============================================================
# 🔹 OPERATORI GEOMETRICI BASE
# ============================================================

def identity(grid: np.ndarray) -> np.ndarray:
    return grid.copy()


def rotate90(grid: np.ndarray) -> np.ndarray:
    return np.rot90(grid, k=1)


def rotate180(grid: np.ndarray) -> np.ndarray:
    return np.rot90(grid, k=2)


def rotate270(grid: np.ndarray) -> np.ndarray:
    return np.rot90(grid, k=3)


def flip_h(grid: np.ndarray) -> np.ndarray:
    return np.fliplr(grid)


def flip_v(grid: np.ndarray) -> np.ndarray:
    return np.flipud(grid)


# ============================================================
# 🔹 OPERATORE DI COLOR MAPPING (STEP 4 ARC)
# ============================================================

def color_map(grid: np.ndarray, mapping: Dict[int, int]) -> np.ndarray:
    """
    Applica una mappatura colore → colore al grid.
    Esempio: {2:5, 3:7}
    """
    out = grid.copy()
    for src, dst in mapping.items():
        out[out == src] = dst
    return out


# ============================================================
# 🔹 REGISTRY OPERATORI GEOMETRICI
# (usato per STEP 1–2–3)
# ============================================================

OPERATORS: List[Callable[[np.ndarray], np.ndarray]] = [
    identity,
    rotate90,
    rotate180,
    rotate270,
    flip_h,
    flip_v,
]

