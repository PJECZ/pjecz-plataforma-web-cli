"""
CLI Domicilios App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_domicilios

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar domicilios"""
    rich.print("Consultar domicilios...")
    try:
        respuesta = get_domicilios(
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Estado", "Municipio", "Calle", "No. Ext.", "No. Int.", "Colonia", "C.P.")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["estado"],
            registro["municipio"],
            registro["calle"],
            registro["num_ext"],
            registro["num_int"],
            registro["colonia"],
            str(registro["cp"]),
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] domicilios")
