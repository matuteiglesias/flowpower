from typing import Optional, Union
from promptflow.client import PFClient
from flowpower.config import _DEFAULTS
from flowpower.logger import logger, log_run
from flowpower.sdk.run_config import build_run_config
from flowpower.sdk.flow_inspect import is_streamable_flow, describe_flow
from flowpower.engine.executor import run_flow_streaming, run_node

from typing import Dict, Any


from flowpower.config import Config

# then later
default_log_level = Config.get("log.level")

import yaml




from promptflow._utils.yaml_utils import load_yaml

from promptflow.core import Prompty

class FlowpowerPrompty:
    def __init__(self, path, model=None):
        self._prompty = Prompty.load(path, model=model)

    def run(self, **inputs):
        return self._prompty(**inputs)

# # Usage:
# flow = FlowpowerPrompty("blocks/hello.prompty")
# out = flow.run(text="python")

from promptflow.contracts.tool import (
    InputDefinition,
    OutputDefinition,
    Tool,
    ValueType,
    ToolType,
)



import os



class FlowpowerClient:
    def __init__(self, config: Optional[dict] = None):
        self._pf = PFClient()
        self._config = config or _DEFAULTS


    def create(
            self,
            file: Optional[str] = None,
            flow: Optional[Union[str, dict]] = None,
            data: Optional[Union[str, dict]] = None,
            stream: bool = False,
            variant: Optional[str] = None,
            resume_from: Optional[str] = None,
            **kwargs
        ):
            """
            Run a flow. Auto-selects batch or streaming based on flow type and flags.
            """
            if file:
                with open(file, 'r') as f:
                    flow = yaml.safe_load(f)
            run_name = kwargs.get("name", "flow_run")
            with log_run(run_name):
                run_config = build_run_config(
                    flow=flow,
                    data=data,
                    stream=stream,
                    variant=variant,
                    resume_from=resume_from,
                    **kwargs,
                )

                kind = detect_kind(run_config)  # e.g., "flow", "batch", "eval"
                if kind == "flow":
                    return self._run_flow(run_config)
                elif kind == "batch":
                    logger.info("📗 Starting batch run...")
                    return self._run_batch(run_config)

                if stream or is_streamable_flow(flow):
                    return run_flow_streaming(flow, data, run_config)
                return self._pf.run(**run_config)

    def run_node(self, flow: str, node_name: str, inputs: dict):
        """
        Run a specific node from a flow in isolation.
        """
        logger.info(f"⚙️ Running node '{node_name}' from flow '{flow}'...")
        return run_node(flow, node_name, inputs)

    def trace(self, run_id: str):
        """
        Retrieve trace info for a given run ID.
        """
        logger.info(f"🔍 Retrieving trace for run ID: {run_id}")
        return self._pf.runs.get(run_id)

    def describe(self, flow: str) -> dict:
        """
        Return flow metadata: inputs, outputs, chat output flag, etc.
        """
        logger.info(f"📋 Describing flow: {flow}")
        return describe_flow(flow)

    def tools(self):
        """
        List available tools registered in PF.
        """
        logger.info("🧰 Listing available tools...")
        return self._pf.tools.list()

    def serve(self, flow: str, port: int = 23333):
        """
        (Optional) Serve the flow using PromptFlow's Flask app.
        """
        from promptflow._sdk._service.app import create_app

        logger.info(f"🌐 Serving flow on http://localhost:{port}")
        app, _ = create_app()
        app.run(port=port, host="0.0.0.0")


    def _run_prompty(
        self,
        config: Union[str, Dict],
        extra_inputs: Dict[str, Any] = None,
        env: Dict[str, str] = None
    ) -> Any:
        """
        Execute a `.prompty` YAML template using PromptFlow's internal Prompty engine.

        Args:
            config (Union[str, dict]): Path to .prompty file or a loaded dict.
            extra_inputs (dict): Additional inputs or overrides to pass to the prompt.
            env (dict): Custom environment variables to use for interpolation.

        Returns:
            Any: The output from the LLM (e.g., string).
        """
        # If config is a path, load YAML
        if isinstance(config, str):
            config_path = config
            config = load_yaml(config_path)
        else:
            config_path = "<inline>"

        if not isinstance(config, dict):
            raise ValueError("Expected a `.prompty` config as dict or file path.")

        # Load Prompty using PromptFlow's main interface
        prompty = Prompty.load(source=config_path, env=env)

        # Merge inputs
        inputs = extra_inputs or {}

        # Execute prompt
        result = prompty(**inputs)

        return result



def detect_kind(config: dict) -> str:
    """
    Detect the kind of run based on the structure of the YAML config.
    
    Returns:
        - "flow": a standard flow run with nodes
        - "batch": batch run over a dataset
        - "eval": evaluation run referencing a previous run
        - "unknown": if none match
    """
    if not isinstance(config, dict):
        return "unknown"
    if "nodes" in config:
        return "flow"
    if "inputs" in config and "model" in config:
        return "prompty"  # NEW
    if "inputs_mapping" in config and "data" in config:
        return "batch"
    elif "metrics" in config and "run" in config:
        logger.info("📙 Detected type: eval")
        return "eval"
    elif config.get("type") in {"standard", "evaluation", "chat"}:
        return "flow"

    return "unknown"




from promptflow.core import Prompty

def prompty_run(path, **inputs):
    """
    Run a .prompty file with the given inputs.

    Args:
        path (str): Path to the .prompty file
        inputs (dict): Keyword arguments matching prompt inputs
    Returns:
        LLM response (string or dict)
    """
    prompty = Prompty.load(source=path)
    return prompty(**inputs)


from promptflow.contracts.tool import Tool, ToolType, InputDefinition, OutputDefinition
from promptflow.core import Prompty

def prompty_to_tool(path: str) -> Tool:
    prompty = Prompty.load(source=path)
    inputs = {
        name: InputDefinition.deserialize(defn)
        for name, defn in prompty._data.get("inputs", {}).items()
    }
    outputs = {
        name: OutputDefinition.deserialize(defn)
        for name, defn in prompty._data.get("outputs", {}).items()
    }
    return Tool(
        name=prompty._name,
        type=ToolType.PROMPT,
        inputs=inputs,
        outputs=outputs,
        source=str(prompty.path),
        description=prompty._data.get("description", ""),
    )
