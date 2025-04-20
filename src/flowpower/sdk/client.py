from typing import Optional, Union
from promptflow.client import PFClient
from flowpower.config import _DEFAULTS
from flowpower.logger import logger, log_run
from flowpower.sdk.run_config import build_run_config
from flowpower.sdk.flow_inspect import is_streamable_flow, describe_flow
from flowpower.engine.executor import run_flow_streaming

from flowpower.config import Config

# then later
default_log_level = Config.get("log.level")


class FlowpowerClient:
    def __init__(self, config: Optional[dict] = None):
        self._pf = PFClient()
        self._config = config or _DEFAULTS

    def run(
        self,
        flow: Union[str, dict],
        data: Optional[Union[str, dict]] = None,
        stream: bool = False,
        variant: Optional[str] = None,
        resume_from: Optional[str] = None,
        **kwargs
    ):
        """
        Run a flow. Auto-selects batch or streaming based on flow type and flags.
        """
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

            if stream or is_streamable_flow(flow):
                return run_flow_streaming(flow, data, run_config)
            return self._pf.run(**run_config)

    def exec_node(self, flow: str, node_name: str, inputs: dict):
        """
        Run a specific node from a flow in isolation.
        """
        logger.info(f"⚙️ Running node '{node_name}' from flow '{flow}'...")
        return exec_node(flow, node_name, inputs)

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
