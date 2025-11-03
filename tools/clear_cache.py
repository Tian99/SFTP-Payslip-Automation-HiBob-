from core.cache import Cache
import os
from core import config

c = Cache(os.getenv("REDIS_URL", config.REDIS_URL))
c.flush()
print("Cache flushed.")
