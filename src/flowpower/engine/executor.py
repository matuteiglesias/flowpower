from typing import Union, Dict, Optional
from pathlib import Path
from promptflow.client import PFClient
from promptflow._proxy import ProxyFactory
from flowpower.logger import logger
from flowpower.sdk.flow_inspect import is_streamable_flow
from flowpower.engine.stream_adapter import stream_output_generator


def run_flow(
    flow: Union[str, Path],
    data: Optional[Union[str, Path]] = None,
    stream: bool = False,
    run_config: Optional[Dict] = None
):
    """
    Run a full flow. Supports streaming if the flow is compatible.

    :param flow: Path to the flow file or directory.
    :param data: Path to the input data (CSV, JSONL, JSON).
    :param stream: Whether to simulate token-by-token streaming output.
    :param run_config: The configuration dictionary passed to PFClient.run().
    :return: A Run object from PromptFlow.
    """
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
    """
    Execute a flow in streaming mode, printing token outputs as they arrive.

    :param flow: Flow file or folder.
    :param data: Data path (ignored if already passed via run_config).
    :param run_config: The configuration for PFClient.run().
    :return: A Run object.
    """
    pf = PFClient()
    run = pf.run(**run_config)

    logger.info("📡 Streaming output tokens:")
    for token in stream_output_generator(run):
        print(token, end="", flush=True)

    print()
    return run


def exec_node(
    flow: Union[str, Path],
    node_name: str,
    inputs: Dict,
    run_id: Optional[str] = None
):
    """
    Run a single node from the flow using async-compatible execution.

    :param flow: Path to the flow definition.
    :param node_name: The name of the node to execute.
    :param inputs: Dictionary of input parameters for the node.
    :param run_id: Optional run context.
    :return: Node output result.
    """
    logger.info(f"🔧 Running single node: {node_name}")
    proxy = ProxyFactory().get_executor_proxy(flow_path=flow)

    # Uses a helper that allows nested event loops
    from flowpower.utils.async_wrap import async_run_allowing_running_loop
    result = async_run_allowing_running_loop(
        proxy.exec_line_async,
        inputs=inputs,
        index=None,
        run_id=run_id,
    )

    logger.info(f"✅ Node executed. Output: {str(result.output)[:80]}")
    return result


def _log_outputs(outputs):
    """
    Display outputs in a human-readable way.
    """
    if isinstance(outputs, dict):
        logger.info("📤 Outputs:")
        for k, v in outputs.items():
            print(f"🔹 {k}: {v}")
    elif isinstance(outputs, list):
        for i, item in enumerate(outputs):
            print(f"🔸 [{i}]: {item}")
    else:
        print(f"📦 {outputs}")
