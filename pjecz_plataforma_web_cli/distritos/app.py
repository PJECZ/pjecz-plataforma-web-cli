"""
CLI Distritos App
"""
import csv
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_distritos

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

    # Solicitar datos
    try:
        respuesta = get_distritos(
            es_distrito=es_distrito,
            es_distrito_judicial=es_distrito_judicial,
            es_jurisdiccional=es_jurisdiccional,
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
            registro["id"],
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
def guardar():
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
            try:
                respuesta = get_distritos(
                    limit=LIMIT,
                    offset=offset,
                )
            except CLIAnyError as error:
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

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] distritos guardados en el archivo {nombre_archivo_csv}")
