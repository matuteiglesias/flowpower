# engine/executor.py

from typing import Union, Dict
from pathlib import Path
from promptflow.client import PFClient
from flowpower.logger import logger

def run_streaming(flow: Union[str, dict], data: Union[str, dict], run_config: Dict):
    """
    Simulate streaming: call PFClient, yield line-by-line if output supports it.
    In future: replace with real token streaming (OpenAI/Anthropic, etc.).
    """
    logger.info("💬 Running flow in streaming mode...")
    pf = PFClient()
    run = pf.run(**run_config)

    # Naively stream line-by-line if output is iterable
    output = run.outputs
    if isinstance(output, dict):
        for k, v in output.items():
            logger.info(f"[{k}] {v}")
        return run
    elif isinstance(output, list):
        for line in output:
            print(line)
        return run
    else:
        print(output)
        return run


def exec_node(flow: Union[str, Path], node_name: str, inputs: dict):
    """
    Run a specific node from a flow.
    """
    pf = PFClient()
    result = pf.runs._run_node(flow=flow, node_name=node_name, inputs=inputs)
    return result
