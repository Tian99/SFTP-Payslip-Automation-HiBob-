from collections import defaultdict
from datetime import datetime

"""
Lightweight in-memory metrics collector (mock Prometheus replacement).
Used for local testing when Prometheus is not available.

- `inc()` increments a counter by key.
- `snapshot()` returns the current state of all counters.
- `metric_event()` produces a timestamped metric event dict (for logging or export).
"""

COUNTERS = defaultdict(int)

def inc(key: str, n: int = 1):
    COUNTERS[key] += n

def snapshot():
    return dict(COUNTERS)

def metric_event(name: str, **labels):
    return {"metric": name, "labels": labels, "ts": datetime.utcnow().isoformat() + "Z"}
