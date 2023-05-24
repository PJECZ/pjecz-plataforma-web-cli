"""
CLI Oficinas App
"""
import csv
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_oficinas

encabezados = ["ID", "Clave", "Distrito", "Edificio", "Descripcion"]

app = typer.Typer()


@app.command()
def consultar(
    distrito_id: int = None,
    distrito_clave: str = None,
    domicilio_id: int = None,
    es_jurisdiccional: bool = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar oficinas"""
    rich.print("Consultar oficinas...")

    # Solicitar datos
    try:
        respuesta = get_oficinas(
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            domicilio_id=domicilio_id,
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
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["distrito_nombre_corto"],
            registro["domicilio_edificio"],
            registro["descripcion_corta"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] oficinas")


@app.command()
def guardar():
    """Guardar oficinas en un archivo CSV"""
    rich.print("Guardar oficinas...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"oficinas_{fecha_hora}.csv"

    # Guardar los datos en un archivo CSV haciendo bucle de consultas a la API
    with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        offset = 0
        while True:
            try:
                respuesta = get_oficinas(
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
                        registro["distrito_nombre_corto"],
                        registro["domicilio_edificio"],
                        registro["descripcion_corta"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] oficinas guardados en el archivo {nombre_archivo_csv}")
