# src/flowpower/cli/__init__.py

from typer import Typer
from . import run, trace, stream, inspect  # ✅ these must all have `app` defined

cli = Typer()

cli.add_typer(run.app, name="run")
cli.add_typer(trace.app, name="trace")
cli.add_typer(stream.app, name="stream")
cli.add_typer(inspect.app, name="inspect")
