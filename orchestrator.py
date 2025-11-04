from pathlib import Path
from typing import Dict, Any
from observibility.logger import logger, with_trace
from middleware.checksum_util import sha256sum
from core.cache import Cache
from middleware.hibob_api_mock import find_employee, upload_payslip
from middleware.notifications import slack_notify
from middleware.storage_mock import encrypt_copy
from observibility.metrics import inc, snapshot
import re, os

"""
Orchestrator — Core workflow manager for payslip processing.

This component coordinates the end-to-end pipeline:
1. Scans payslip PDFs in a folder.
2. Deduplicates using checksum and Redis cache.
3. Parses employee metadata from filename (e.g., EMP001_202511.pdf).
4. Uploads each payslip to the (mocked) HR API with retry logic.
5. Archives successfully processed files.
6. Emits metrics and logs for observability and FinOps tracking.

Key integrations:
- Cache (Redis or in-memory)
- HiBob API mock for uploads
- Slack notifications for errors and success
- Prometheus-style counters via `observibility.metrics`
"""

EMP_RE = re.compile(r"^(?P<emp>[A-Za-z0-9]+)_(?P<ym>\d{6})\.pdf$")

class Orchestrator:
    def __init__(self, employees: Dict[str, Any], cache: Cache, archive_dir: str,
                 fail_rate: float, max_attempts: int, base_delay: float):
        self.employees = employees
        self.cache = cache
        self.archive_dir = archive_dir
        self.fail_rate = fail_rate
        self.max_attempts = max_attempts
        self.base_delay = base_delay

    def parse_meta(self, file_path: str) -> Dict[str, str] | None:
        name = Path(file_path).name
        m = EMP_RE.match(name)
        if not m:
            return None
        return {"employee_id": m.group("emp"), "period": m.group("ym")}

    def process_file(self, file_path: str):
        filename = Path(file_path).name
        ctx = with_trace({"file": file_path})
        logger.info(f"🏁 Processing {filename} ...", **ctx)

        checksum = sha256sum(file_path)
        dedup_key = f"checksum:{checksum}"
        if self.cache.get(dedup_key):
            inc("dedup_skipped_total")
            short_sum = checksum[:12]
            logger.info(f"⚠️  Duplicate skipped (checksum={short_sum}…)", **ctx)
            return

        meta = self.parse_meta(file_path)
        if not meta:
            inc("parse_error_total")
            logger.error(f"❌ Invalid filename format: {filename}", **ctx)
            return

        emp = find_employee(self.employees, meta["employee_id"])
        if not emp:
            inc("employee_not_found_total")
            logger.error(f"❌ Employee not found: {meta['employee_id']}", **ctx)
            return

        from core.retry_handler import retry
        def do_upload():
            res = upload_payslip(emp["hibob_id"], file_path, self.fail_rate)
            if res.get("status") != "ok":
                raise RuntimeError(res.get("message", "upload failed"))
            return res

        try:
            res = retry(do_upload, self.max_attempts, self.base_delay)
        except Exception as e:
            inc("upload_final_fail_total")
            logger.error(f"❌ Upload failed for {filename}: {e}", **ctx)
            slack_notify(f"❌ Upload failed for {filename}", error=str(e))
            return

        archive_path = encrypt_copy(file_path, self.archive_dir)
        self.cache.set(dedup_key, "1")

        inc("upload_success_total")
        logger.info(f"✅ Uploaded {filename} → {archive_path}", **ctx)
        slack_notify(f"✅ Uploaded {filename}", employee=meta["employee_id"], period=meta["period"])

    def run_folder(self, folder: str):
        p = Path(folder)
        files = sorted([str(x) for x in p.glob("*.pdf")])
        if not files:
            logger.warning(f"⚠️  No PDF files found in {folder}")
            return
        for f in files:
            self.process_file(f)
        metrics = snapshot()
        logger.info(f"🧾 Run complete — metrics={metrics}")