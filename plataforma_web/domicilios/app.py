"""
CLI Domicilios App
"""
import csv
from datetime import datetime
import time

import rich
import typer

from config.settings import LIMIT, SLEEP
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Distrito", "Edificio", "Calle", "No. Ext.", "No. Int.", "Colonia", "Municipio", "C.P."]

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar domicilios"""
    rich.print("Consultar domicilios...")

    # Consultar a la API
    try:
        respuesta = requests_get(
            subdirectorio="domicilios",
            parametros={"limit": limit, "offset": offset},
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
            registro["distrito_clave"],
            registro["edificio"],
            registro["calle"],
            registro["num_ext"],
            registro["num_int"],
            registro["colonia"],
            registro["municipio"],
            str(registro["cp"]),
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] domicilios")


@app.command()
def guardar():
    """Guardar domicilios en un archivo CSV"""
    rich.print("Guardar domicilios...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"domicilios_{fecha_hora}.csv"

    # Guardar los datos en un archivo CSV haciendo bucle de consultas a la API
    with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        offset = 0
        while True:
            try:
                respuesta = requests_get(
                    subdirectorio="distritos",
                    parametros={"limit": LIMIT, "offset": offset},
                )
            except MyAnyError as error:
                typer.secho(str(error), fg=typer.colors.RED)
                raise typer.Exit()
            for registro in respuesta["items"]:
                escritor.writerow(
                    [
                        registro["id"],
                        registro["distrito_clave"],
                        registro["edificio"],
                        registro["calle"],
                        registro["num_ext"],
                        registro["num_int"],
                        registro["colonia"],
                        registro["municipio"],
                        registro["cp"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break
            rich.print(f"Van [green]{offset}[/green] domicilios...")
            time.sleep(SLEEP)

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] domicilios guardados en el archivo {nombre_archivo_csv}")
