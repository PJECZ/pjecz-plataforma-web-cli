"""
CLI Centros de Trabajo App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_centros_trabajos

app = typer.Typer()


@app.command()
def consultar(
    distrito_id: int = None,
    domicilio_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar centros de trabajo"""
    rich.print("Consultar centros de trabajo...")
    try:
        respuesta = get_centros_trabajos(
            distrito_id=distrito_id,
            domicilio_id=domicilio_id,
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Clave", "Nombre", "Distrito", "Domicilio", "Telefono")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["nombre"],
            registro["distrito_nombre_corto"],
            registro["domicilio_completo"],
            registro["telefono"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] centros de trabajo")
