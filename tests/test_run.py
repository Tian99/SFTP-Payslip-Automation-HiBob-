"""
Integration test for Orchestrator.run_folder() with mock files.
"""
import os
from orchestrator import Orchestrator
from core.cache import Cache
from core import config


def test_run_folder(tmp_path):
    """Simulate running orchestrator with dummy files"""
    dummy = tmp_path / "EMP001_202501.pdf"
    dummy.write_bytes(b"mock-pdf")

    orch = Orchestrator(
        employees={"EMP001": {"hibob_id": "H001"}},
        cache=Cache(None),
        archive_dir=str(tmp_path / "archive"),
        fail_rate=0.0,
        max_attempts=1,
        base_delay=0.1,
    )

    orch.run_folder(str(tmp_path))
    assert os.path.exists(tmp_path / "archive" / "EMP001_202501.pdf")