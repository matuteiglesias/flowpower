import typer
from flowpower.sdk.client import FlowpowerClient

app = typer.Typer()

@app.command(name="inspect")
def cli(flow: str):
    """
    Describe the inputs/outputs of a flow.
    """
    client = FlowpowerClient()
    schema = client.describe(flow)
    typer.echo(schema)
