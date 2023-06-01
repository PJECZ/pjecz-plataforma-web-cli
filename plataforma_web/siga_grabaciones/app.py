"""
CLI SIGA Grabaciones App
"""
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_siga_grabaciones

encabezados = ["ID", "Inicio", "Sala", "Autoridad", "Expediente", "Duración", "Tamaño", "Estado"]

app = typer.Typer()


@app.command()
def consultar(
    distrito_id: int = None,
    distrito_clave: str = None,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    siga_sala_id: int = None,
    siga_sala_clave: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar grabaciones"""
    rich.print("Consultar grabaciones...")

    # Solicitar datos
    try:
        respuesta = get_siga_grabaciones(
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            siga_sala_id=siga_sala_id,
            siga_sala_clave=siga_sala_clave,
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for enca in encabezados:
        table.add_column(enca)
    for registro in respuesta["items"]:
        inicio = datetime.strptime(registro["inicio"], "%Y-%m-%dT%H:%M:%S")
        tamanio = f"{registro['tamanio'] / (1024 * 1024):0.2f} MB"
        estado = registro["estado"]
        if estado == "VALIDO":
            estado = "[cyan] " + estado
        table.add_row(
            str(registro["id"]),
            inicio.strftime("%Y-%m-%d %H:%M:%S"),
            registro["siga_sala_clave"],
            registro["autoridad_clave"],
            registro["expediente"],
            registro["duracion"],
            tamanio,
            estado,
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] grabaciones")
