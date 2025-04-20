# cli/trace.py

import typer
from flowpower.sdk.client import FlowpowerClient
from flowpower.engine.trace_utils import pretty_print_trace

app = typer.Typer()

@app.command()
def cli(run_id: str):
    """
    Retrieve and print a human-readable trace summary.
    """
    client = FlowpowerClient()
    run = client.trace(run_id)
    pretty_print_trace(run)
