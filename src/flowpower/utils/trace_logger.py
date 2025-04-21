# flowpower/utils/trace_logger.py

import json
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

# Logger setup
logger = logging.getLogger("flowpower.trace")
logger.setLevel(logging.INFO)

LOG_DIR = Path(".fp_logs")
LOG_DIR.mkdir(exist_ok=True)
log_file_path = LOG_DIR / "run.log"

# Log to file and stdout
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(console_handler)


# --- Simple Logging Helpers ---
def log_step(step: str, inputs: dict, outputs: dict = None):
    """
    Log a short one-liner summary of a successful step.
    """
    out_str = _short_repr(outputs) if outputs is not None else "(no output)"
    logger.info(f"✅ [{step}] ← {out_str}")


def log_error(step: str, err: Exception):
    """
    Log a short one-liner summary of an error at a step.
    """
    logger.error(f"❌ [{step}] Error: {type(err).__name__}: {str(err)}")


def dump_json(run_id: str, step: str, inputs: dict, outputs: dict = None):
    """
    Dump full inputs and outputs to a JSON file under logs.
    """
    trace_dir = LOG_DIR / run_id
    trace_dir.mkdir(parents=True, exist_ok=True)
    fpath = trace_dir / f"{step}.json"
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump({"inputs": inputs, "outputs": outputs}, f, indent=2, ensure_ascii=False)


# --- Streaming ---
def stream_logs():
    """
    Tail the run log file for live watching.
    """
    import subprocess
    subprocess.run(["tail", "-f", str(log_file_path)])


# --- Internal Helper ---
def _short_repr(data: dict, max_len=100):
    try:
        s = json.dumps(data)
        return s if len(s) <= max_len else s[:max_len] + "..."
    except Exception:
        return str(data)
