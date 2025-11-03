import json, os
import click
from core.cache import Cache
from orchestrator import Orchestrator
from observibility.logger import logger
from dotenv import load_dotenv
from core import config
from middleware.sftp_listener import list_payslips

load_dotenv(override=True)

def load_employees(path="data/employees.json"):
    with open(path, "r") as f:
        return json.load(f)

@click.group()
def cli():
    pass

@cli.command()
@click.option("--input", "-i", default="data/payslips", help="Folder containing payslips")
@click.option("--fail-rate", type=float, default=None, help="Override failure rate [0..1]")
def run(input, fail_rate):
    employees = load_employees()
    cache = Cache(os.getenv("REDIS_URL", config.REDIS_URL))
    rate = config.FAIL_RATE if fail_rate is None else fail_rate
    orch = Orchestrator(
        employees=employees,
        cache=cache,
        archive_dir=config.ARCHIVE_DIR,
        fail_rate=rate,
        max_attempts=config.RETRY_MAX_ATTEMPTS,
        base_delay=config.RETRY_BASE_DELAY,
    )
    files = list_payslips(input)
    if not files:
        logger.info("no_files_found", folder=input)
    orch.run_folder(input)

if __name__ == "__main__":
    cli()
