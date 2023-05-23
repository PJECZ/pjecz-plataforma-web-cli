"""
CLI Inv Custodias App
"""
import csv
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_inv_custodias

encabezados = ["ID", "Creado", "Usuario", "Nombre completo"]

app = typer.Typer()


@app.command()
def consultar(
    fecha_desde: str = None,
    fecha_hasta: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar custodias"""
    rich.print("Consultar custodias...")

    # Solicitar datos
    try:
        respuesta = get_inv_custodias(
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
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
            registro["usuario_email"],
            registro["nombre_completo"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] custodias")


@app.command()
def guardar(
    fecha_desde: str = None,
    fecha_hasta: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
):
    """Guardar custodias en un archivo CSV"""
    rich.print("Guardar custodias...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"inv_custodias_{fecha_hora}.csv"

    # Guardar los datos en un archivo CSV haciendo bucle de consultas a la API
    with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        offset = 0
        while True:
            try:
                respuesta = get_inv_custodias(
                    fecha_desde=fecha_desde,
                    fecha_hasta=fecha_hasta,
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
                        registro["usuario_email"],
                        registro["nombre_completo"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] custodias guardados en el archivo {nombre_archivo_csv}")
