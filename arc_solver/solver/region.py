import numpy as np
from typing import Tuple, Optional

# ============================================================
# BOUNDING BOX
# ============================================================

def find_bbox(
    grid: np.ndarray, background: int = 0
) -> Optional[Tuple[int, int, int, int]]:
    """
    Trova il bounding box dei pixel != background.

    Ritorna:
        (r_min, r_max, c_min, c_max) inclusivi
    Se non trova nulla, ritorna None.
    """
    coords = np.where(grid != background)
    if coords[0].size == 0:
        return None

    r_min, r_max = coords[0].min(), coords[0].max()
    c_min, c_max = coords[1].min(), coords[1].max()
    return r_min, r_max, c_min, c_max


def crop(
    grid: np.ndarray,
    bbox: Tuple[int, int, int, int],
) -> np.ndarray:
    """Ritaglia la griglia usando un bounding box (inclusivo)."""
    r_min, r_max, c_min, c_max = bbox
    return grid[r_min : r_max + 1, c_min : c_max + 1]


def bbox_crop(
    grid: np.ndarray,
    background: int = 0,
) -> np.ndarray:
    """
    Operatore ARC:
    - ritaglia il bounding box minimo dei pixel != background
    - se non esiste, ritorna la griglia originale
    """
    bbox = find_bbox(grid, background)
    if bbox is None:
        return grid.copy()
    return crop(grid, bbox)

# ============================================================
# TRANSLATION (STEP 8)
# ============================================================

def translate_bbox(
    bbox: Tuple[int, int, int, int],
    dr: int,
    dc: int,
    shape: Tuple[int, int],
) -> Optional[Tuple[int, int, int, int]]:
    """
    Trasla un bbox di (dr, dc) e verifica che rimanga dentro la griglia.
    """
    r_min, r_max, c_min, c_max = bbox

    nr_min = r_min + dr
    nr_max = r_max + dr
    nc_min = c_min + dc
    nc_max = c_max + dc

    H, W = shape
    if nr_min < 0 or nc_min < 0 or nr_max >= H or nc_max >= W:
        return None

    return nr_min, nr_max, nc_min, nc_max

# ============================================================
# PASTE
# ============================================================

def paste(
    base: np.ndarray,
    patch: np.ndarray,
    bbox: Tuple[int, int, int, int],
    background: int = 0,
) -> np.ndarray:
    """
    Incolla patch in base usando bbox.
    I pixel == background NON vengono incollati.
    """
    r_min, r_max, c_min, c_max = bbox
    out = base.copy()

    mask = patch != background
    out[r_min : r_max + 1, c_min : c_max + 1][mask] = patch[mask]
    return out

