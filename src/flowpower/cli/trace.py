# cli/trace.py

import typer
from flowpower.sdk.client import FlowpowerClient

app = typer.Typer()

@app.command()
def cli(run_id: str):
    """
    Retrieve and print trace for a run.
    """
    client = FlowpowerClient()
    trace = client.trace(run_id)
    typer.echo(trace)
