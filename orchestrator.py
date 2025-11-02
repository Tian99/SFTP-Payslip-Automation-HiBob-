from pathlib import Path
from typing import Dict, Any
from logger import logger, with_trace
from checksum_util import sha256sum
from cache import Cache
from hibob_api_mock import find_employee, upload_payslip
from notifications import slack_notify
from storage_mock import encrypt_copy
from metrics import inc, snapshot
import re

EMP_RE = re.compile(r"^(?P<emp>[A-Za-z0-9]+)_(?P<ym>\d{6})\.pdf$")

class Orchestrator:
    def __init__(self, employees: Dict[str, Any], cache: Cache, archive_dir: str, fail_rate: float, max_attempts: int, base_delay: float):
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
        ctx = with_trace({"file": file_path})
        logger.info("processing_start", **ctx)

        checksum = sha256sum(file_path)
        dedup_key = f"checksum:{checksum}"
        if self.cache.get(dedup_key):
            inc("dedup_skipped_total")
            logger.info("dedup_skipped", checksum=checksum, **ctx)
            return

        meta = self.parse_meta(file_path)
        if not meta:
            inc("parse_error_total")
            logger.error("filename_parse_failed", **ctx)
            return

        emp = find_employee(self.employees, meta["employee_id"])
        if not emp:
            inc("employee_not_found_total")
            logger.error("employee_not_found", employee_id=meta["employee_id"], **ctx)
            return

        from retry_handler import retry
        def do_upload():
            res = upload_payslip(emp["hibob_id"], file_path, self.fail_rate)
            if res.get("status") != "ok":
                raise RuntimeError(res.get("message", "upload failed"))
            return res

        try:
            res = retry(do_upload, self.max_attempts, self.base_delay)
        except Exception as e:
            inc("upload_final_fail_total")
            logger.error("upload_error", error=str(e), **ctx)
            slack_notify(f"Upload failed for {file_path}", error=str(e))
            return

        archive_path = encrypt_copy(file_path, self.archive_dir)
        self.cache.set(dedup_key, "1")

        inc("upload_success_total")
        logger.info("processing_done", result=res, archive=archive_path, **ctx)
        slack_notify(f"Uploaded {Path(file_path).name}", employee=meta["employee_id"], period=meta["period"])

    def run_folder(self, folder: str):
        p = Path(folder)
        files = sorted([str(x) for x in p.glob("*.pdf")])
        for f in files:
            self.process_file(f)
        logger.info("run_complete", metrics=snapshot())
