"""
CLI SIGA Grabaciones App
"""
from datetime import datetime, timedelta

import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Archivo Nombre", "Inicio", "Sala", "Autoridad", "Expediente", "Duración", "Tamaño"]

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

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if autoridad_id is not None:
        parametros["autoridad_id"] = autoridad_id
    if autoridad_clave is not None:
        parametros["autoridad_clave"] = autoridad_clave
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    if distrito_clave is not None:
        parametros["distrito_clave"] = distrito_clave
    if materia_id is not None:
        parametros["materia_id"] = materia_id
    if materia_clave is not None:
        parametros["materia_clave"] = materia_clave
    if siga_sala_id is not None:
        parametros["siga_sala_id"] = siga_sala_id
    if siga_sala_clave is not None:
        parametros["siga_sala_clave"] = siga_sala_clave
    try:
        respuesta = requests_get(
            subdirectorio="siga_grabaciones",
            parametros=parametros,
        )
    except MyAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for enca in encabezados:
        table.add_column(enca)
    for registro in respuesta["items"]:
        inicio_datetime = datetime.fromisoformat(registro["inicio"].replace("Z", "+00:00"))
        duracion_segundos = timedelta(seconds=registro["duracion"])
        table.add_row(
            str(registro["id"]),
            registro["archivo_nombre"],
            inicio_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            registro["siga_sala_clave"],
            registro["autoridad_clave"],
            registro["expediente"],
            f"{duracion_segundos} seg.",
            f"{registro['tamanio'] / (1024 * 1024):0.2f} MB",
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] grabaciones")
