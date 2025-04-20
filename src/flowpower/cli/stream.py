import typer

app = typer.Typer()

@app.command()
def cli():
    typer.echo("Stream not implemented yet")
