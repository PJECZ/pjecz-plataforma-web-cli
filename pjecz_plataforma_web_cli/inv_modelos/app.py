"""
CLI Inv Modelos App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_inv_modelos

app = typer.Typer()


@app.command()
def consultar(
    inv_marca_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar modelos"""
    rich.print("Consultar modelos...")
    try:
        respuesta = get_inv_modelos(
            inv_marca_id=inv_marca_id,
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Marca", "Descripcion")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["inv_marca_nombre"],
            registro["descripcion"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] modelos")
