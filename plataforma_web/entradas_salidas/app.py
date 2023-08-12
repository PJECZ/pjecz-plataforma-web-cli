"""
CLI Entradas-Salidas App
"""
import csv
from datetime import datetime
import time

import rich
import typer

from config.settings import LIMIT, SLEEP
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Creado", "email", "Tipo", "Direccion IP"]

app = typer.Typer()


@app.command()
def consultar(
    usuario_id: int = None,
    usuario_email: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar entradas-salidas"""
    rich.print("Consultar entradas-salidas...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if usuario_id is not None:
        parametros["usuario_id"] = usuario_id
    if usuario_email is not None:
        parametros["usuario_email"] = usuario_email
    try:
        respuesta = requests_get(
            subdirectorio="entradas_salidas",
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
            registro["usuario_email"],
            registro["tipo"],
            registro["direccion_ip"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] entradas-salidas")


@app.command()
def guardar(
    usuario_id: int = None,
    usuario_email: str = None,
):
    """ Guardar entradas-salidas en un archivo CSV """
    rich.print("Guardar entradas-salidas...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"entradas_salidas_{fecha_hora}.csv"

    # Guardar los datos en un archivo CSV haciendo bucle de consultas a la API
    with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        offset = 0
        while True:
            parametros = {"limit": LIMIT, "offset": offset}
            if usuario_id is not None:
                parametros["usuario_id"] = usuario_id
            if usuario_email is not None:
                parametros["usuario_email"] = usuario_email
            try:
                respuesta = requests_get(
                    subdirectorio="entradas_salidas",
                    parametros=parametros,
                )
            except MyAnyError as error:
                typer.secho(str(error), fg=typer.colors.RED)
                raise typer.Exit()
            for registro in respuesta["items"]:
                creado_datetime = datetime.fromisoformat(registro["creado"].replace("Z", "+00:00"))
                escritor.writerow([
                    str(registro["id"]),
                    creado_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    registro["usuario_email"],
                    registro["tipo"],
                    registro["direccion_ip"],
                ])
            offset += LIMIT
            if offset >= respuesta["total"]:
                break
            rich.print(f"Van [green]{offset}[/green] entradas-salidas...")
            time.sleep(SLEEP)

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] entradas-salidas guardados en el archivo {nombre_archivo_csv}")
