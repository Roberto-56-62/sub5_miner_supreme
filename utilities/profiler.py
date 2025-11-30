import time

def profile(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        r = func(*args, **kwargs)
        t1 = time.time()
        print(f"[PROFILE] {func.__name__} → {t1 - t0:.4f}s")
        return r
    return wrapper

