from pathlib import Path
from typing import List

def list_payslips(folder: str) -> List[str]:
    p = Path(folder)
    return [str(f) for f in p.glob("*.pdf")]
