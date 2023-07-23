from datetime import datetime, timedelta
from functools import lru_cache, wraps
from threading import Lock


def cache(seconds: int, max_size: int = 128, typed: bool = False):
    """有効期限付きキャッシュ"""

    def wrapper(f):
        func = lru_cache(maxsize=max_size, typed=typed)(f)
        func.ttl = seconds
        func.expire = datetime.utcnow() + timedelta(seconds=func.ttl)

        @wraps(f)
        def inner(*args, **kwargs):
            with Lock():
                if datetime.utcnow() > func.expire:
                    func.cache_clear()
                    func.expire = datetime.utcnow() + timedelta(seconds=func.ttl)
                return func(*args, **kwargs)

        inner.clear_cache = func.cache_clear
        inner.cache_info = func.cache_info
        return inner

    return wrapper
