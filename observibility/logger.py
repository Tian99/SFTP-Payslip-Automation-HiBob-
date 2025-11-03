from loguru import logger
import sys
import uuid
import os
from datetime import datetime

ENV = os.getenv("ENV", "local").lower()

logger.remove()

if ENV in ("local", "dev"):
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | "
               "<cyan>{message}</cyan> <dim>{extra}</dim>",
        level="INFO",
        enqueue=False,
    )
else:
    logger.add(
        sys.stdout,
        serialize=True,
        enqueue=True,
        level="INFO",
    )

def with_trace(extra=None):
    base = {"trace_id": str(uuid.uuid4()), "ts": datetime.utcnow().isoformat() + "Z"}
    if extra:
        base.update(extra)
    return base