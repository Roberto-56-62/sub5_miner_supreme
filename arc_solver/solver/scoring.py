# ============================================================
# SCORING – ARC Solver
# ============================================================

import numpy as np


def score_grid(predicted: np.ndarray, target: np.ndarray) -> float:
    """
    Score semplice e robusto:
    - 1.0 = match perfetto
    - 0.0 = completamente sbagliato
    """

    if predicted.shape != target.shape:
        return 0.0

    total = predicted.size
    correct = np.sum(predicted == target)

    return correct / total

