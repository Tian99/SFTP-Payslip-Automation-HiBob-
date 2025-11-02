from cache import Cache
import os, config

c = Cache(os.getenv("REDIS_URL", config.REDIS_URL))
c.flush()
print("Cache flushed.")
