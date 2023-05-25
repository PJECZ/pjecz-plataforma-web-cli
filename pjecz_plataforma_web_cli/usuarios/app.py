"""
CLI Usuarios App
"""
import csv
from datetime import datetime
import time

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT, SLEEP

from .request_api import get_usuarios

encabezados = ["ID", "Distrito", "Autoridad", "Oficina", "email", "Nombres", "A. Paterno", "A. Materno", "Workspace"]

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    workspace: str = None,
    offset: int = 0,
    limit: int = LIMIT,
):
    """Consultar usuarios"""
    rich.print("Consultar usuarios...")

    # Solicitar datos
    try:
        respuesta = get_usuarios(
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            workspace=workspace,
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
            str(registro["id"]),
            registro["distrito_nombre_corto"],
            registro["autoridad_descripcion_corta"],
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
            try:
                respuesta = get_usuarios(
                    autoridad_id=autoridad_id,
                    autoridad_clave=autoridad_clave,
                    oficina_id=oficina_id,
                    oficina_clave=oficina_clave,
                    workspace=workspace,
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
                        registro["distrito_nombre_corto"],
                        registro["autoridad_descripcion_corta"],
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
