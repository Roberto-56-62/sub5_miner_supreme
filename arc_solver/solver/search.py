from typing import List, Callable, Optional
import numpy as np
from .scoring import exact_match

def search(
    inp: np.ndarray,
    train_pairs: List[tuple],
    operators: List[Callable[[np.ndarray], np.ndarray]],
    max_depth: int = 2,
) -> Optional[Callable[[np.ndarray], np.ndarray]]:
    # depth 1
    for op in operators:
        ok = True
        for tin, tout in train_pairs:
            try:
                if not exact_match(op(tin), tout):
                    ok = False
                    break
            except Exception:
                ok = False
                break
        if ok:
            return op

    # depth 2 (composition)
    if max_depth >= 2:
        for op1 in operators:
            for op2 in operators:
                ok = True
                for tin, tout in train_pairs:
                    try:
                        if not exact_match(op2(op1(tin)), tout):
                            ok = False
                            break
                    except Exception:
                        ok = False
                        break
                if ok:
                    return lambda x, a=op1, b=op2: b(a(x))

    return None

