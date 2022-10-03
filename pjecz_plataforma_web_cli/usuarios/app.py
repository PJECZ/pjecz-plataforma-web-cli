"""
CLI Usuarios App
"""
import csv
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_usuarios

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    limit: int = LIMIT,
    guardar: bool = False,
    oficina_id: int = None,
    oficina_clave: str = None,
    offset: int = 0,
    workspace: str = None,
):
    """Consultar usuarios"""
    rich.print("Consultar usuarios...")

    # Solicitar datos
    try:
        respuesta = get_usuarios(
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            limit=limit,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            offset=offset,
            workspace=workspace,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Encabezados
    encabezados = ["ID", "Distrito", "Autoridad", "Oficina", "email", "Nombres", "A. Paterno", "A. Materno", "Workspace"]

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
        rich.print(f"Datos guardados en el archivo {nombre_archivo_csv}")

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
