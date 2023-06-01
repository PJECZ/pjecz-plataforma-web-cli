"""
CLI Inv Redes App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_inv_redes

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar redes"""
    rich.print("Consultar redes...")
    try:
        respuesta = get_inv_redes(
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Nombre", "Tipo")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["nombre"],
            registro["tipo"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] redes")
