"""
CLI Permisos App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_permisos

app = typer.Typer()


@app.command()
def consultar(
    modulo_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
    rol_id: int = None,
):
    """Consultar permisos"""
    rich.print("Consultar permisos...")
    try:
        respuesta = get_permisos(
            modulo_id=modulo_id,
            limit=limit,
            offset=offset,
            rol_id=rol_id,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Rol", "Modulo", "Nivel")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["rol_nombre"],
            registro["modulo_nombre"],
            str(registro["nivel"]),
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] permisos")
