from loguru import logger
import sys
import uuid
from datetime import datetime

logger.remove()
logger.add(sys.stdout, serialize=True, enqueue=True, level="INFO")

def with_trace(extra=None):
    base = {"trace_id": str(uuid.uuid4()), "ts": datetime.utcnow().isoformat() + "Z"}
    if extra:
        base.update(extra)
    return base
