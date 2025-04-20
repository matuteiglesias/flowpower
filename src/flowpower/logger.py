import logging
import sys
import time
from contextlib import contextmanager
from datetime import datetime

try:
    from rich.logging import RichHandler
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def get_logger(name="flowpower", level=logging.INFO):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Prevent duplicate handlers

    if RICH_AVAILABLE and sys.stderr.isatty():
        handler = RichHandler(markup=True, rich_tracebacks=True)
        formatter = logging.Formatter("%(message)s")
    else:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("🌊 [%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S")

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False  # Avoid double logging

    return logger


logger = get_logger()


def log_start(run_name: str):
    logger.info(f"🚀 Starting run: [bold cyan]{run_name}[/bold cyan] at {datetime.now().isoformat(timespec='seconds')}")


def log_end(run_name: str, success: bool = True, start_time: float = None):
    emoji = "✅" if success else "❌"
    duration = f"{time.time() - start_time:.2f}s" if start_time else "?"
    logger.info(f"{emoji} Finished run: [bold cyan]{run_name}[/bold cyan] in {duration}")


@contextmanager
def log_run(run_name: str):
    log_start(run_name)
    start = time.time()
    try:
        yield
        log_end(run_name, success=True, start_time=start)
    except Exception as e:
        log_end(run_name, success=False, start_time=start)
        logger.exception(f"❗ Run {run_name} failed due to an exception.")
        raise
