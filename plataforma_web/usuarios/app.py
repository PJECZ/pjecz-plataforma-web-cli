"""
CLI Usuarios App
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
    "Distrito",
    "Autoridad",
    "Oficina",
    "email",
    "Nombres",
    "A. Paterno",
    "A. Materno",
    "Workspace",
]

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    workspace: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar usuarios"""
    rich.print("Consultar usuarios...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if autoridad_id is not None:
        parametros["autoridad_id"] = autoridad_id
    if autoridad_clave is not None:
        parametros["autoridad_clave"] = autoridad_clave
    if oficina_id is not None:
        parametros["oficina_id"] = oficina_id
    if oficina_clave is not None:
        parametros["oficina_clave"] = oficina_clave
    if workspace is not None:
        parametros["workspace"] = workspace
    try:
        respuesta = requests_get(
            subdirectorio="usuarios",
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
            registro["distrito_clave"],
            registro["autoridad_clave"],
            registro["oficina_clave"],
            registro["email"],
            registro["nombres"],
            registro["apellido_paterno"],
            registro["apellido_materno"],
            registro["workspace"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] usuarios")


@app.command()
def guardar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    workspace: str = None,
):
    """Guardar usuarios en un archivo CSV"""
    rich.print("Guardar usuarios...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"usuarios_{fecha_hora}.csv"

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
            if oficina_id is not None:
                parametros["oficina_id"] = oficina_id
            if oficina_clave is not None:
                parametros["oficina_clave"] = oficina_clave
            if workspace is not None:
                parametros["workspace"] = workspace
            try:
                respuesta = requests_get(
                    subdirectorio="usuarios",
                    parametros=parametros,
                )
            except MyAnyError as error:
                typer.secho(str(error), fg=typer.colors.RED)
                raise typer.Exit()
            for registro in respuesta["items"]:
                escritor.writerow(
                    [
                        str(registro["id"]),
                        registro["distrito_clave"],
                        registro["autoridad_clave"],
                        registro["oficina_clave"],
                        registro["email"],
                        registro["nombres"],
                        registro["apellido_paterno"],
                        registro["apellido_materno"],
                        registro["workspace"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break
            rich.print(f"Van [green]{offset}[/green] usuarios...")
            time.sleep(SLEEP)

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] usuarios guardados en el archivo {nombre_archivo_csv}")
