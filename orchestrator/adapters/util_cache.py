import time
from functools import wraps

def ttl_cache(ttl_seconds=60):
    def deco(fn):
        cache = {}
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in cache:
                v, ts = cache[key]
                if now - ts < ttl_seconds:
                    return v
            v = fn(*args, **kwargs)
            cache[key] = (v, now)
            return v
        return wrapper
    return deco
