import numpy as np
from typing import List, Dict

def to_array(grid: List[List[int]]) -> np.ndarray:
    return np.array(grid, dtype=int)

def same_shape(a: np.ndarray, b: np.ndarray) -> bool:
    return a.shape == b.shape

def colors(grid: np.ndarray) -> set:
    return set(int(x) for x in np.unique(grid))

