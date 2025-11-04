import os

"""
Configuration module — loads environment variables with sane defaults.
Used to control Redis connection, archive paths, retry behavior, and
failure simulation rate for the orchestration pipeline.
"""

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
ARCHIVE_DIR = os.getenv("ARCHIVE_DIR", "../data/archive")
MAX_QPS_PER_EMPLOYEE = float(os.getenv("MAX_QPS_PER_EMPLOYEE", "3"))
RETRY_MAX_ATTEMPTS = int(os.getenv("RETRY_MAX_ATTEMPTS", "3"))
RETRY_BASE_DELAY = float(os.getenv("RETRY_BASE_DELAY", "0.5"))
FAIL_RATE = float(os.getenv("FAIL_RATE", "0.0"))
