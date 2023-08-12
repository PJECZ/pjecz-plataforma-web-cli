"""
CLI Sentencias App
"""
from datetime import datetime

import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = [
    "ID",
    "Creado",
    "Autoridad",
    "Materia",
    "Tipo de Juicio",
    "Sentencia",
    "Sentencia F.",
    "Expediente",
    "Fecha",
    "Es P.G.",
    "Archivo",
]

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
    materia_tipo_juicio_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar sentencias"""
    rich.print("Consultar sentencias...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if autoridad_id is not None:
        parametros["autoridad_id"] = autoridad_id
    if autoridad_clave is not None:
        parametros["autoridad_clave"] = autoridad_clave
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    if fecha is not None:
        parametros["fecha"] = fecha
    if fecha_desde is not None:
        parametros["fecha_desde"] = fecha_desde
    if fecha_hasta is not None:
        parametros["fecha_hasta"] = fecha_hasta
    if materia_tipo_juicio_id is not None:
        parametros["materia_tipo_juicio_id"] = materia_tipo_juicio_id
    try:
        respuesta = requests_get(
            subdirectorio="sentencias",
            parametros=parametros,
        )
    except MyAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for registro in respuesta["items"]:
        creado_datetime = datetime.fromisoformat(registro["creado"].replace("Z", "+00:00"))
        table.add_row(
            str(registro["id"]),
            creado_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            registro["autoridad_clave"],
            registro["materia_nombre"],
            registro["materia_tipo_juicio_descripcion"],
            registro["sentencia"],
            registro["sentencia_fecha"],
            registro["expediente"],
            registro["fecha"],
            "SI" if registro["es_perspectiva_genero"] else "NO",
            registro["archivo"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] sentencias")
