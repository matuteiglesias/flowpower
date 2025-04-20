import yaml
from typing import Union
from pathlib import Path


def is_streamable_flow(flow: Union[str, dict]) -> bool:
    """
    Naive check: is the flow structured to support token streaming?
    """
    try:
        flow_dict = _load_flow(flow)
    except Exception:
        return False

    for node in flow_dict.get("nodes", []):
        if "stream" in str(node).lower():
            return True
    return False


def describe_flow(flow: Union[str, dict]) -> dict:
    """
    Extract flow schema info: inputs, outputs, streaming flag.
    """
    flow_dict = _load_flow(flow)

    return {
        "inputs": flow_dict.get("inputs", {}),
        "outputs": flow_dict.get("outputs", {}),
        "nodes": [n["name"] for n in flow_dict.get("nodes", [])],
        "is_streamable": is_streamable_flow(flow),
    }


def _load_flow(flow: Union[str, dict]) -> dict:
    """
    Internal helper to load a flow from YAML path or raw dict.
    """
    if isinstance(flow, dict):
        return flow
    flow_path = Path(flow).resolve()
    with open(flow_path, "r") as f:
        return yaml.safe_load(f)
