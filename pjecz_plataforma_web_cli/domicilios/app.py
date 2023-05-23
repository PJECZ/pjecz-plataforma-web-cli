"""
CLI Domicilios App
"""
import csv
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_domicilios

app = typer.Typer()


@app.command()
def consultar(
    guardar: bool = False,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar domicilios"""
    rich.print("Consultar domicilios...")

    # Solicitar datos
    try:
        respuesta = get_domicilios(
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Encabezados
    encabezados = ["ID", "Edificio", "Estado", "Municipio", "Calle", "No. Ext.", "No. Int.", "Colonia", "C.P."]

    # Guardar datos en un archivo CSV
    if guardar:
        fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo_csv = f"usuarios_{fecha_hora}.csv"
        with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezados)
            for registro in respuesta["items"]:
                escritor.writerow(
                    [
                        registro["id"],
                        registro["edificio"],
                        registro["estado"],
                        registro["municipio"],
                        registro["calle"],
                        registro["num_ext"],
                        registro["num_int"],
                        registro["colonia"],
                        registro["cp"],
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
            registro["edificio"],
            registro["estado"],
            registro["municipio"],
            registro["calle"],
            registro["num_ext"],
            registro["num_int"],
            registro["colonia"],
            str(registro["cp"]),
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] domicilios")
