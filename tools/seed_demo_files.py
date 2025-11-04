from pathlib import Path
from datetime import datetime

"""
Utility script to generate mock payslip PDF files for testing.
Each file is named as EMP<ID>_<YYYYMM>.pdf and placed under data/payslips/.
The content is a minimal fake PDF header — just for simulation purposes.
"""

base = Path("data/payslips")
base.mkdir(parents=True, exist_ok=True)

def make_pdf(name: str):
    p = base / name
    with p.open("wb") as f:
        f.write(b"%PDF-1.4\n% Mock PDF\n")
    print("created", p)

def main():
    ym = datetime.utcnow().strftime("%Y%m")
    for emp in ["EMP001","EMP002","EMP003"]:
        make_pdf(f"{emp}_{ym}.pdf")

if __name__ == "__main__":
    main()
