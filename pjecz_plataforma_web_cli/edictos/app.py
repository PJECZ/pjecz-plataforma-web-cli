"""
CLI Edictos App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_edictos

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    fecha: str = None,
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar edictos"""
    rich.print("Consultar edictos...")
    try:
        respuesta = get_edictos(
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Autoridad", "Fecha", "Descripcion", "Expediente", "No. Pub.", "Archivo")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["autoridad_clave"],
            registro["fecha"],
            registro["descripcion"],
            registro["expediente"],
            registro["numero_publicacion"],
            registro["archivo"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] edictos")
