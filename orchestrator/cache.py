import time
from functools import wraps

def ttl_cache(ttl_seconds=30):
    def deco(fn):
        store = {}
        @wraps(fn)
        def wrapped(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in store:
                val, ts = store[key]
                if now - ts < ttl_seconds:
                    return val
            val = fn(*args, **kwargs)
            store[key] = (val, now)
            return val
        return wrapped
    return deco
