"""
CLI Bitacoras App
"""
import csv
import time
from datetime import datetime

import rich
import typer

from config.settings import LIMIT, SLEEP
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Creado", "Modulo", "email", "Descripcion"]

app = typer.Typer()


@app.command()
def consultar(
    modulo_id: int = None,
    modulo_nombre: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar bitacoras"""
    rich.print("Consultar bitacoras...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if modulo_id is not None:
        parametros["modulo_id"] = modulo_id
    if modulo_nombre is not None:
        parametros["modulo_nombre"] = modulo_nombre
    if usuario_id is not None:
        parametros["usuario_id"] = usuario_id
    if usuario_email is not None:
        parametros["usuario_email"] = usuario_email
    try:
        respuesta = requests_get(
            subdirectorio="bitacoras",
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
            registro["modulo_nombre"],
            registro["usuario_email"],
            registro["descripcion"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] bitacoras")


@app.command()
def guardar(
    modulo_id: int = None,
    modulo_nombre: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
):
    """Guardar bitacoras en un archivo CSV"""
    rich.print("Guardar bitacoras...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"bitacoras_{fecha_hora}.csv"

    # Guardar los datos en un archivo CSV haciendo bucle de consultas a la API
    with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        offset = 0
        while True:
            parametros = {"limit": LIMIT, "offset": offset}
            if modulo_id is not None:
                parametros["modulo_id"] = modulo_id
            if modulo_nombre is not None:
                parametros["modulo_nombre"] = modulo_nombre
            if usuario_id is not None:
                parametros["usuario_id"] = usuario_id
            if usuario_email is not None:
                parametros["usuario_email"] = usuario_email
            try:
                respuesta = requests_get(
                    subdirectorio="bitacoras",
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
                        registro["modulo_nombre"],
                        registro["usuario_email"],
                        registro["descripcion"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break
            rich.print(f"Van [green]{offset}[/green] bitacoras...")
            time.sleep(SLEEP)

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] bitacoras guardados en el archivo {nombre_archivo_csv}")
