import random
from typing import Dict, Any
from observibility.logger import logger
from observibility.metrics import inc

def find_employee(employees: dict, employee_id: str) -> Dict[str, Any] | None:
    return employees.get(employee_id)

def upload_payslip(hibob_id: str, file_path: str, fail_rate: float = 0.0) -> dict:
    if random.random() < fail_rate:
        inc("hibob_upload_fail_total")
        logger.error("hibob_upload_failed", hibob_id=hibob_id, file=file_path)
        return {"status": "error", "message": "Simulated failure"}
    inc("hibob_upload_success_total")
    logger.info("hibob_upload_ok", hibob_id=hibob_id, file=file_path)
    return {"status": "ok", "hibob_id": hibob_id}
