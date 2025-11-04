from core.cache import Cache
import os
from core import config

"""
Utility script to clear the Redis (or in-memory) cache.
Used to reset deduplication and rate-limiting state during local testing.
"""

c = Cache(os.getenv("REDIS_URL", config.REDIS_URL))
c.flush()
print("Cache flushed.")
