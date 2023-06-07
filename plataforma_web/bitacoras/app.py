"""
CLI Bitacoras App
"""
import csv
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_bitacoras

encabezados = ["ID", "Creado", "Clave", "Descripcion"]

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

    # Solicitar datos
    try:
        respuesta = get_bitacoras(
            modulo_id=modulo_id,
            modulo_nombre=modulo_nombre,
            usuario_id=usuario_id,
            usuario_email=usuario_email,
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
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["clave"],
            registro["descripcion"],
            "SI" if registro["es_x"] else "NO",
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
            try:
                respuesta = get_bitacoras(
                    modulo_id=modulo_id,
                    modulo_nombre=modulo_nombre,
                    usuario_id=usuario_id,
                    usuario_email=usuario_email,
                    limit=LIMIT,
                    offset=offset,
                )
            except CLIAnyError as error:
                typer.secho(str(error), fg=typer.colors.RED)
                raise typer.Exit()
            for registro in respuesta["items"]:
                creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
                escritor.writerow(
                    [
                        registro["id"],
                        creado.strftime("%Y-%m-%d %H:%M:%S"),
                        registro["clave"],
                        registro["descripcion"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] bitacoras guardados en el archivo {nombre_archivo_csv}")
