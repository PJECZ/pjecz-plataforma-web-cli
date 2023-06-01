"""
CLI Edictos App
"""
import csv
from datetime import datetime
import time

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT, SLEEP

from .request_api import get_edictos

encabezados = ["ID", "Creado", "Autoridad", "Fecha", "Descripcion", "Expediente", "No. Pub.", "Archivo"]

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    fecha: str = None,
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar edictos"""
    rich.print("Consultar edictos...")

    # Solicitar datos
    try:
        respuesta = get_edictos(
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
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
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f%z")  # %z: UTC offset in the form +HHMM or -HHMM (empty string if the object is naive).
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["autoridad_clave"],
            registro["fecha"],
            registro["descripcion"],
            registro["expediente"],
            registro["numero_publicacion"],
            registro["archivo"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] edictos")


@app.command()
def guardar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    fecha: str = None,
    fecha_desde: str = None,
    fecha_hasta: str = None,
):
    """Guardar edictos en un archivo CSV"""
    rich.print("Guardar edictos...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"edictos_{fecha_hora}.csv"

    # Guardar los datos en un archivo CSV haciendo bucle de consultas a la API
    with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        offset = 0
        while True:
            try:
                respuesta = get_edictos(
                    autoridad_id=autoridad_id,
                    autoridad_clave=autoridad_clave,
                    fecha=fecha,
                    fecha_desde=fecha_desde,
                    fecha_hasta=fecha_hasta,
                    limit=LIMIT,
                    offset=offset,
                )
            except CLIAnyError as error:
                typer.secho(str(error), fg=typer.colors.RED)
                raise typer.Exit()
            for registro in respuesta["items"]:
                creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f%z")  # %z: UTC offset in the form +HHMM or -HHMM (empty string if the object is naive).
                escritor.writerow(
                    [
                        registro["id"],
                        creado.strftime("%Y-%m-%d %H:%M:%S"),
                        registro["autoridad_clave"],
                        registro["fecha"],
                        registro["descripcion"],
                        registro["expediente"],
                        registro["numero_publicacion"],
                        registro["archivo"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break
            rich.print(f"Van [green]{offset}[/green] edictos...")
            time.sleep(SLEEP)

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] edictos guardados en el archivo {nombre_archivo_csv}")
