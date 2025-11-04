import hashlib
from pathlib import Path

"""
Utility function — computes the SHA256 checksum of a file.
Used to verify file integrity and detect duplicates during processing.
"""

def sha256sum(path: str) -> str:
    p = Path(path)
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
