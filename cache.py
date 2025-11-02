from typing import Optional
from contextlib import suppress

try:
    import redis
except Exception:
    redis = None

from logger import logger

class Cache:
    def __init__(self, url: str | None):
        self._inmem = {}
        self._r = None
        if url and redis:
            with suppress(Exception):
                self._r = redis.Redis.from_url(url, decode_responses=True)
                self._r.ping()
                logger.info("redis_connected", url=url)

    def get(self, key: str) -> Optional[str]:
        if self._r:
            return self._r.get(key)
        return self._inmem.get(key)

    def set(self, key: str, value: str, ex: int | None = None):
        if self._r:
            self._r.set(key, value, ex=ex)
        else:
            self._inmem[key] = value

    def incr(self, key: str, n: int = 1):
        if self._r:
            return self._r.incrby(key, n)
        self._inmem[key] = int(self._inmem.get(key, 0)) + n
        return self._inmem[key]

    def flush(self):
        if self._r:
            self._r.flushdb()
        else:
            self._inmem.clear()
