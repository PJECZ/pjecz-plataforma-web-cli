"""
CLI SIGA Grabaciones App
"""
import csv
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_siga_grabaciones

encabezados = ["ID", "Distrito", "Sala", "Autoridad", "Archivo", "Duracion", "Tamanio", "Inicio", "Expediente"]

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    materia_id: int = None,
    materia_clave: str = None,
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
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            materia_id=materia_id,
            materia_clave=materia_clave,
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
        table.add_row(
            str(registro["id"]),
            registro["distrito_clave"],
            registro["siga_sala_clave"],
            registro["autoridad_clave"],
            registro["archivo_nombre"],
            str(registro["duracion"]),
            str(registro["tamanio"]),
            registro["inicio"],
            registro["expediente"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] grabaciones")
