import os
import time
import json
import threading
from pathlib import Path
from typing import Any, Dict

from promptflow.executor._prompty_executor import PromptyExecutor
from promptflow.executor._script_executor import ScriptExecutor

from flowpower.logger import logger
from flowpower.utils.trace_logger import log_step, log_error, dump_json
from flowpower.utils.env_utils import resolve_env_vars


# Optional live log watcher
def maybe_tail_logs(watch: bool):
    if watch:
        def tail_log():
            os.system("tail -f logs/run.log")
        threading.Thread(target=tail_log).start()


# Dump trace for each step
def dump_trace_to_file(run_id, step_name, inputs, outputs):
    trace_dir = Path(".fp_trace_logs") / run_id
    trace_dir.mkdir(parents=True, exist_ok=True)
    trace_file = trace_dir / f"{step_name}.json"
    with open(trace_file, "w") as f:
        json.dump({"inputs": inputs, "outputs": outputs}, f, indent=2)


# ----------------------------------------
# FlowpowerScriptExecutor
# ----------------------------------------
class FlowpowerScriptExecutor(ScriptExecutor):
    def _initialize_function(self):
        logger.info("🧠 Initializing function from flow...")
        return super()._initialize_function()

    def execute(self, inputs, **kwargs):
        logger.info(f"⚙️ Executing with inputs: {inputs}")
        return super().execute(inputs, **kwargs)

    def exec_line(self, inputs, **kwargs):
        logger.info(f"⚙️ Flowpower executing line with: {inputs}")
        return super().exec_line(inputs, **kwargs)

    def _exec_line(self, inputs, index=None, run_id=None, allow_generator_output=False):
        logger.info(f"🔸 Executing line {index or '?'} with inputs: {inputs}")
        try:
            output = super()._exec_line(inputs, index, run_id, allow_generator_output)
            dump_trace_to_file(run_id or "no_id", f"line_{index}", inputs, output.output)
            logger.info(f"✅ Output from line {index}: {output.output}")
            return output
        except Exception as e:
            log_error("flow", f"line_{index}", inputs, error=e)
            raise


# ----------------------------------------
# FlowpowerPromptyExecutor
# ----------------------------------------
class FlowpowerPromptyExecutor(PromptyExecutor):
    """
    A Flowpower-enhanced PromptyExecutor.
    Adds extra logging, environment resolution, and trace output.
    """

    def _initialize_function(self):
        logger.info(f"🧠 Initializing Prompty '{self.prompty._name}' with Flowpower logic...")
        return super()._initialize_function()

    def execute(self, inputs: Dict[str, Any], **kwargs):
        logger.info(f"🧠 Running prompty '{self.prompty._name}' with inputs: {inputs}")

        try:
            inputs = resolve_env_vars(inputs)
            result = super().execute(inputs, **kwargs)

            log_step("prompty", self.prompty._name, inputs, result)
            self._dump_output(inputs, result)

            logger.info(f"✅ Prompty result: {result}")
            return result

        except Exception as e:
            log_error("prompty", self.prompty._name, inputs, error=e)
            raise

    def explain(self, inputs: Dict[str, Any]) -> str:
        return self.prompty.render(**inputs)

    def estimate(self, inputs: Dict[str, Any]) -> int:
        count = self.prompty.estimate_token_count(**inputs)
        logger.info(f"🧠 Estimated token count: {count}")
        return count

    def explain_prompt(self, inputs: Dict[str, Any]) -> str:
        return self.prompty.render(**inputs)

    def get_signature(self) -> Dict[str, Any]:
        return {
            "inputs": self._inputs,
            "raw_yaml": self.prompty._data.get("inputs", {})
        }

    def _dump_output(self, inputs, result):
        filename = f"outputs/{self.prompty._name}_{int(time.time())}.json"
        Path("outputs/").mkdir(exist_ok=True)
        with open(filename, "w") as f:
            json.dump({"inputs": inputs, "output": result}, f, indent=2)
