import time
from observibility.logger import logger

"""
Retry utility — executes a function with exponential backoff.
Used to handle transient failures (e.g., network or API errors)
by retrying a fixed number of times before raising the exception.
"""

def retry(fn, attempts: int, base_delay: float, *args, **kwargs):
    last = None
    for i in range(1, attempts + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            last = e
            logger.warning("retry_attempt", attempt=i, error=str(e))
            time.sleep(base_delay * (2 ** (i - 1)))
    if last:
        raise last
