"""
CLI Listas de Acuerdos App
"""
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_listas_de_acuerdos

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    fecha: str = None,
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar listas de acuerdos"""
    rich.print("Consultar listas de acuerdos...")
    try:
        respuesta = get_listas_de_acuerdos(
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
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
    table = rich.table.Table("ID", "Creado", "Autoridad", "Fecha", "Descripcion", "Archivo")
    for registro in respuesta["items"]:
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f%z")  # %z: UTC offset in the form +HHMM or -HHMM (empty string if the object is naive).
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["autoridad_clave"],
            registro["fecha"],
            registro["descripcion"],
            registro["archivo"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] listas de acuerdos")
