import typer

app = typer.Typer()

@app.command(name="stream")
def cli():
    typer.echo("Stream not implemented yet")
