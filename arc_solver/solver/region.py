import numpy as np
from typing import Tuple


def find_bbox(grid: np.ndarray, background: int = 0) -> Tuple[int, int, int, int] | None:
    """
    Trova bounding box dei pixel != background
    Ritorna (r_min, r_max, c_min, c_max) inclusivi
    """
    coords = np.where(grid != background)
    if coords[0].size == 0:
        return None

    r_min, r_max = coords[0].min(), coords[0].max()
    c_min, c_max = coords[1].min(), coords[1].max()
    return r_min, r_max, c_min, c_max


def crop(grid: np.ndarray, bbox) -> np.ndarray:
    r_min, r_max, c_min, c_max = bbox
    return grid[r_min : r_max + 1, c_min : c_max + 1]


def paste(
    base: np.ndarray, patch: np.ndarray, bbox, background: int = 0
) -> np.ndarray:
    r_min, r_max, c_min, c_max = bbox
    out = base.copy()
    mask = patch != background
    out[r_min : r_max + 1, c_min : c_max + 1][mask] = patch[mask]
    return out

