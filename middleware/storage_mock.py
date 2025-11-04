from pathlib import Path
from shutil import copy2
from observibility.logger import logger

"""
Mock storage module.
Simulates encryption and archiving of processed payslips by copying them into an archive folder.
In a real system, this step would perform encryption and secure upload to cloud/object storage.
"""

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

def encrypt_copy(src: str, dst_dir: str) -> str:
    ensure_dir(dst_dir)
    target = Path(dst_dir) / Path(src).name
    copy2(src, target)
    logger.info("archive_written", path=str(target))
    return str(target)
