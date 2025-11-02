from collections import defaultdict
from datetime import datetime

COUNTERS = defaultdict(int)

def inc(key: str, n: int = 1):
    COUNTERS[key] += n

def snapshot():
    return dict(COUNTERS)

def metric_event(name: str, **labels):
    return {"metric": name, "labels": labels, "ts": datetime.utcnow().isoformat() + "Z"}
