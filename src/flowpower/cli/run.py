import typer
from typing import Optional, List

from flowpower.sdk.client import FlowpowerClient
from flowpower.utils.parse_kv import parse_kv_pairs
from flowpower.logger import logger

app = typer.Typer()


@app.command(name="run")
def main(
    flow: str = typer.Argument(..., help="Path to flow file (.yaml or Prompty)"),
    data: Optional[str] = typer.Option(None, help="Path to data (CSV, JSONL, or inline JSON)"),
    stream: bool = typer.Option(False, help="Stream output (for chat flows)"),
    variant: Optional[str] = typer.Option(None, help="Flow variant name"),
    resume_from: Optional[str] = typer.Option(None, help="Resume from a previous run ID"),
    column_mapping: Optional[List[str]] = typer.Option(None, help="Map input columns (e.g. question=prompt)"),
    init: Optional[List[str]] = typer.Option(None, help="Init parameters (e.g. key=value)"),
    name: Optional[str] = typer.Option(None, help="Custom run name"),
    trace: bool = typer.Option(False, help="Print trace after run (if available)"),
):
    """
    Run a flow with optional data input, streaming, or config overrides.
    """
    logger.info("🌊 Flowpower: Starting flow run...")
    client = FlowpowerClient()

    column_mapping_dict = parse_kv_pairs(column_mapping)
    init_kwargs = parse_kv_pairs(init)

    try:
        run = client.run(
            flow=flow,
            data=data,
            stream=stream,
            variant=variant,
            resume_from=resume_from,
            column_mapping=column_mapping_dict,
            init=init_kwargs,
            name=name,
        )
        typer.echo(f"✅ Run submitted: {getattr(run, 'name', 'unnamed')}")

        if trace and hasattr(run, "name"):
            typer.echo("🔍 Fetching trace...")
            trace_output = client.trace(run.name)
            typer.echo(trace_output)

    except Exception as e:
        logger.error(f"❌ Flow run failed: {e}")
        raise typer.Exit(code=1)
