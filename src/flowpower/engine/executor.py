import os
import json
from pathlib import Path
from typing import Union, Dict, Optional

from promptflow.client import PFClient
from promptflow._sdk._configuration import Configuration
from promptflow._proxy import ProxyFactory
from promptflow.storage._run_storage import DefaultRunStorage
from promptflow._utils.flow_utils import is_prompty_flow
from promptflow._utils.logger_utils import logger

from flowpower.logger import logger
from flowpower.sdk.flow_inspect import is_streamable_flow
from flowpower.engine.stream_adapter import stream_output_generator
from flowpower.utils.async_wrap import async_run_allowing_running_loop

from flowpower.engine.runner import FlowpowerScriptExecutor, FlowpowerPromptyExecutor


# --------------------------------------
# Script & Prompty Executors
# --------------------------------------

def run_prompty_native(path: Union[str, Path], inputs: Dict):
    executor = FlowpowerPromptyExecutor(flow_file=path)
    executor.initialize()
    return executor.execute(inputs)


def run_script_flow(path: Union[str, Path], inputs: Dict):
    executor = FlowpowerScriptExecutor(flow_file=path)
    executor.initialize()
    return executor.execute(inputs)


def run_flex_script(path: Union[str, Path], inputs: Dict):
    executor = FlowpowerScriptExecutor(flow_file=path)
    return executor.exec_line(inputs).output


# --------------------------------------
# Proxy Utilities for Node Execution
# --------------------------------------

def get_executor_proxy(flow_path: Union[str, Path]):
    flow_path = Path(flow_path).resolve()
    working_dir = flow_path.parent
    flow_file = flow_path.name
    language = "python"

    storage = DefaultRunStorage(
        base_dir=Path(".flow_runs"),
        sub_dir=Path("temp")
    )

    proxy = ProxyFactory().create_executor_proxy(
        flow_file=flow_file,
        working_dir=working_dir,
        connections={},
        storage=storage,
        language=language,
        init_kwargs={}
    )
    return proxy


def run_node(flow: Union[str, Path], node_name: str, inputs: Dict, run_id: Optional[str] = None):
    logger.info(f"🔧 Running single node: {node_name}")
    proxy = get_executor_proxy(flow)
    result = async_run_allowing_running_loop(
        proxy.exec_line_async,
        inputs=inputs,
        run_id=run_id,
    )
    logger.info(f"✅ Node executed. Output: {str(result.output)[:80]}")
    return result


# --------------------------------------
# Full Flow Execution via PFClient
# --------------------------------------

def run_flow(
    flow: Union[str, Path],
    data: Optional[Union[str, Path]] = None,
    stream: bool = False,
    run_config: Optional[Dict] = None
):
    logger.info("🧠 Starting flow execution...")

    if stream and is_streamable_flow(flow):
        logger.info("💬 Flow is streamable. Launching in streaming mode...")
        return run_flow_streaming(flow, data, run_config)

    logger.info("⚙️ Running batch flow with PromptFlow client...")
    pf = PFClient()
    run = pf.run(**run_config)

    _log_outputs(run.outputs)
    return run


def run_flow_streaming(flow: Union[str, Path], data: Optional[Union[str, Path]], run_config: Optional[Dict]):
    pf = PFClient()
    run = pf.run(**run_config)

    logger.info("📡 Streaming output tokens:")
    for token in stream_output_generator(run):
        print(token, end="", flush=True)
    print()
    return run


# --------------------------------------
# Output Utility
# --------------------------------------

def _log_outputs(outputs):
    if isinstance(outputs, dict):
        logger.info("📤 Outputs:")
        for k, v in outputs.items():
            print(f"🔹 {k}: {v}")
    elif isinstance(outputs, list):
        for i, item in enumerate(outputs):
            print(f"🔸 [{i}]: {item}")
    else:
        print(f"📦 {outputs}")
