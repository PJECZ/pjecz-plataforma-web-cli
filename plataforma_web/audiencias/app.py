"""
CLI Audiencias App
"""
import csv
import time
from datetime import datetime

import rich
import typer

from config.settings import LIMIT, SLEEP
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = [
    "ID",
    "Creado",
    "Autoridad",
    "Tipo",
    "Expediente",
    "Actores",
    "Demandados",
    "Sala",
    "Caracter",
    "Causa penal",
    "Delitos",
    "Toca",
    "Exp. origen",
    "Imputados",
    "Origen",
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
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar audiencias"""
    rich.print("Consultar audiencias...")

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
    try:
        respuesta = requests_get(
            subdirectorio="audiencias",
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
        creado_datetime = datetime.fromisoformat(registro["creado"].replace("Z", "+00:00"))
        table.add_row(
            str(registro["id"]),
            creado_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            registro["autoridad_clave"],
            registro["tipo_audiencia"],
            registro["expediente"],
            registro["actores"],
            registro["demandados"],
            registro["sala"],
            registro["caracter"],
            registro["causa_penal"],
            registro["delitos"],
            registro["toca"],
            registro["expediente_origen"],
            registro["imputados"],
            registro["origen"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] audiencias")


@app.command()
def guardar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    fecha: str = None,
    fecha_desde: str = None,
    fecha_hasta: str = None,
):
    """Guardar audiencias en un archivo CSV"""
    rich.print("Guardar audiencias...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"audiencias_{fecha_hora}.csv"

    # Guardar los datos en un archivo CSV haciendo bucle de consultas a la API
    with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        offset = 0
        while True:
            parametros = {"limit": LIMIT, "offset": offset}
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
            try:
                respuesta = requests_get(
                    subdirectorio="audiencias",
                    parametros=parametros,
                )
            except MyAnyError as error:
                typer.secho(str(error), fg=typer.colors.RED)
                raise typer.Exit()
            for registro in respuesta["items"]:
                creado_datetime = datetime.fromisoformat(registro["creado"].replace("Z", "+00:00"))
                escritor.writerow(
                    [
                        str(registro["id"]),
                        creado_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                        registro["autoridad_clave"],
                        registro["tipo_audiencia"],
                        registro["expediente"],
                        registro["actores"],
                        registro["demandados"],
                        registro["sala"],
                        registro["caracter"],
                        registro["causa_penal"],
                        registro["delitos"],
                        registro["toca"],
                        registro["expediente_origen"],
                        registro["imputados"],
                        registro["origen"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break
            rich.print(f"Van [green]{offset}[/green] audiencias...")
            time.sleep(SLEEP)

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] audiencias guardados en el archivo {nombre_archivo_csv}")
