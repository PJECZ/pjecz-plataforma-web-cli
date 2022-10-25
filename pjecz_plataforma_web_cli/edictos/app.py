"""
CLI Edictos App
"""
import csv
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_edictos

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    fecha: str = None,
    fecha_desde: str = None,
    fecha_hasta: str = None,
    guardar: bool = False,
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

    # Encabezados
    encabezados = ["ID", "Autoridad", "Fecha", "Descripcion", "Expediente", "No. Pub.", "Archivo"]

    # Guardar datos en un archivo CSV
    if guardar:
        fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo_csv = f"inv_equipos_{fecha_hora}.csv"
        with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezados)
            for registro in respuesta["items"]:
                escritor.writerow(
                    [
                        registro["id"],
                        registro["autoridad_clave"],
                        registro["fecha"],
                        registro["descripcion"],
                        registro["expediente"],
                        registro["numero_publicacion"],
                        registro["archivo"],
                    ]
                )
        rich.print(f"Datos guardados en el archivo {nombre_archivo_csv}")

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for enca in encabezados:
        table.add_column(enca)
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
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
