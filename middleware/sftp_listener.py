from pathlib import Path
from typing import List

"""
Utility function to list all payslip PDF files in a given folder.
Used by the orchestrator to discover incoming files for processing.
"""

def list_payslips(folder: str) -> List[str]:
    p = Path(folder)
    return [str(f) for f in p.glob("*.pdf")]
