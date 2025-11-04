from loguru import logger
import sys
import uuid
import os
from datetime import datetime, UTC

"""
Centralized logging configuration using Loguru.
- Provides colorized console logs in local/dev environments.
- Switches to structured JSON logs in production for ingestion by ELK/Loki.
- Includes a helper `with_trace()` to attach trace_id and timestamp to log context.
"""

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
    base = {"trace_id": str(uuid.uuid4()), "ts": datetime.now(UTC).isoformat()}
    if extra:
        base.update(extra)
    return base