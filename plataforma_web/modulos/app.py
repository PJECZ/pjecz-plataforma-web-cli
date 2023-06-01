"""
CLI Modulos App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_modulos

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar modulos"""
    rich.print("Consultar modulos...")
    try:
        respuesta = get_modulos(
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Nombre", "Nombre corto", "Icono", "Ruta", "En N.")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["nombre"],
            registro["nombre_corto"],
            registro["icono"],
            registro["ruta"],
            "SI" if registro["en_navegacion"] else "NO",
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] modulos")
