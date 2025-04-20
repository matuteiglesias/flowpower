import typer
from flowpower.sdk.client import FlowpowerClient
from flowpower.engine.trace_utils import pretty_print_trace

app = typer.Typer()

@app.command(name="run")
def trace_run(run_id: str):
    """
    Show a detailed trace summary for a run.
    """
    client = FlowpowerClient()
    run = client.trace(run_id)
    pretty_print_trace(run)

@app.command(name="delete")
def trace_delete(
    run_id: str = typer.Option(None, help="Run ID to delete traces from"),
    collection: str = typer.Option(None, help="Trace collection to delete"),
    started_before: str = typer.Option(None, help="Delete traces before this ISO date"),
    yes: bool = typer.Option(False, help="Skip confirmation"),
):
    """
    Delete traces by run, collection, or timestamp.
    """
    from promptflow._sdk._pf_client import PFClient
    client = PFClient()

    if not yes:
        dry = client.traces.delete(run=run_id, collection=collection, started_before=started_before, dry_run=True)
        typer.confirm(f"This will delete {dry} traces. Continue?", abort=True)

    deleted = client.traces.delete(run=run_id, collection=collection, started_before=started_before)
    typer.echo(f"✅ Deleted {deleted} traces.")
