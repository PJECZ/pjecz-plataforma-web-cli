"""
CLI Distritos App
"""
import csv
from datetime import datetime
import time

import rich
import typer

from config.settings import LIMIT, SLEEP
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Clave", "Nombre", "Nombre Corto", "Es D.", "Es J.", "Es D.J."]

app = typer.Typer()


@app.command()
def consultar(
    es_distrito: bool = None,
    es_distrito_judicial: bool = None,
    es_jurisdiccional: bool = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar distritos"""
    rich.print("Consultar distritos...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if es_distrito is not None:
        parametros["es_distrito"] = es_distrito
    if es_distrito_judicial is not None:
        parametros["es_distrito_judicial"] = es_distrito_judicial
    if es_jurisdiccional is not None:
        parametros["es_jurisdiccional"] = es_jurisdiccional
    try:
        respuesta = requests_get(
            subdirectorio="distritos",
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
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["nombre"],
            registro["nombre_corto"],
            "SI" if registro["es_distrito"] else "",
            "SI" if registro["es_jurisdiccional"] else "",
            "SI" if registro["es_distrito_judicial"] else "",
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] distritos")


@app.command()
def guardar(
    es_distrito: bool = None,
    es_distrito_judicial: bool = None,
    es_jurisdiccional: bool = None,
):
    """Guardar distritos en un archivo CSV"""
    rich.print("Guardar distritos...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"distritos_{fecha_hora}.csv"

    # Guardar los datos en un archivo CSV haciendo bucle de consultas a la API
    with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        offset = 0
        while True:
            parametros = {"limit": LIMIT, "offset": offset}
            if es_distrito is not None:
                parametros["es_distrito"] = es_distrito
            if es_distrito_judicial is not None:
                parametros["es_distrito_judicial"] = es_distrito_judicial
            if es_jurisdiccional is not None:
                parametros["es_jurisdiccional"] = es_jurisdiccional
            try:
                respuesta = requests_get(
                    subdirectorio="distritos",
                    parametros=parametros,
                )
            except MyAnyError as error:
                typer.secho(str(error), fg=typer.colors.RED)
                raise typer.Exit()
            for registro in respuesta["items"]:
                escritor.writerow(
                    [
                        registro["id"],
                        registro["clave"],
                        registro["nombre"],
                        registro["nombre_corto"],
                        "SI" if registro["es_distrito"] else "",
                        "SI" if registro["es_jurisdiccional"] else "",
                        "SI" if registro["es_distrito_judicial"] else "",
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break
            rich.print(f"Van [green]{offset}[/green] distritos...")
            time.sleep(SLEEP)

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] distritos guardados en el archivo {nombre_archivo_csv}")
