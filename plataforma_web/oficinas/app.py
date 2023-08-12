"""
CLI Oficinas App
"""
import csv
import time
from datetime import datetime

import rich
import typer

from config.settings import LIMIT, SLEEP
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Clave", "Distrito", "Edificio", "Descripcion"]

app = typer.Typer()


@app.command()
def consultar(
    distrito_id: int = None,
    distrito_clave: str = None,
    domicilio_id: int = None,
    es_jurisdiccional: bool = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar oficinas"""
    rich.print("Consultar oficinas...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    if distrito_clave is not None:
        parametros["distrito_clave"] = distrito_clave
    if domicilio_id is not None:
        parametros["domicilio_id"] = domicilio_id
    if es_jurisdiccional is not None:
        parametros["es_jurisdiccional"] = es_jurisdiccional
    try:
        respuesta = requests_get(
            subdirectorio="modulos",
            parametros=parametros,
        )
    except MyAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["distrito_nombre_corto"],
            registro["domicilio_edificio"],
            registro["descripcion_corta"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] oficinas")


@app.command()
def guardar(
    distrito_id: int = None,
    distrito_clave: str = None,
    domicilio_id: int = None,
    es_jurisdiccional: bool = None,
):
    """Guardar oficinas en un archivo CSV"""
    rich.print("Guardar oficinas...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"oficinas_{fecha_hora}.csv"

    # Guardar los datos en un archivo CSV haciendo bucle de consultas a la API
    with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        offset = 0
        while True:
            parametros = {"limit": LIMIT, "offset": offset}
            if distrito_id is not None:
                parametros["distrito_id"] = distrito_id
            if distrito_clave is not None:
                parametros["distrito_clave"] = distrito_clave
            if domicilio_id is not None:
                parametros["domicilio_id"] = domicilio_id
            if es_jurisdiccional is not None:
                parametros["es_jurisdiccional"] = es_jurisdiccional
            try:
                respuesta = requests_get(
                    subdirectorio="modulos",
                    parametros=parametros,
                )
            except MyAnyError as error:
                typer.secho(str(error), fg=typer.colors.RED)
                raise typer.Exit()
            for registro in respuesta["items"]:
                escritor.writerow(
                    [
                        str(registro["id"]),
                        registro["clave"],
                        registro["distrito_nombre_corto"],
                        registro["domicilio_edificio"],
                        registro["descripcion_corta"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break
            rich.print(f"Van [green]{offset}[/green] oficinas...")
            time.sleep(SLEEP)

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] oficinas guardados en el archivo {nombre_archivo_csv}")
