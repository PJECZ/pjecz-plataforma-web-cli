"""
CLI Materias Tipos de Juicios App
"""
import csv
import time
from datetime import datetime

import rich
import typer

from config.settings import LIMIT, SLEEP
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Materia", "Descripcion"]

app = typer.Typer()


@app.command()
def consultar(
    materia_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar tipos de juicios"""
    rich.print("Consultar tipos de juicios...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if materia_id is not None:
        parametros["materia_id"] = materia_id
    try:
        respuesta = requests_get(
            subdirectorio="materias_tipos_juicios",
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
            registro["materia_nombre"],
            registro["descripcion"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] tipos de juicios")


@app.command()
def guardar():
    """Guardar tipos de juicios en un archivo CSV"""
    rich.print("Guardar tipos de juicios...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"materias_tipos_juicios_{fecha_hora}.csv"

    # Guardar los datos en un archivo CSV haciendo bucle de consultas a la API
    with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        offset = 0
        while True:
            parametros = {"limit": LIMIT, "offset": offset}
            try:
                respuesta = requests_get(
                    subdirectorio="materias_tipos_juicios",
                    parametros=parametros,
                )
            except MyAnyError as error:
                typer.secho(str(error), fg=typer.colors.RED)
                raise typer.Exit()
            for registro in respuesta["items"]:
                escritor.writerow(
                    [
                        str(registro["id"]),
                        registro["materia_nombre"],
                        registro["descripcion"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break
            rich.print(f"Van [green]{offset}[/green] tipos de juicios...")
            time.sleep(SLEEP)

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] tipos de juicios guardados en el archivo {nombre_archivo_csv}")
