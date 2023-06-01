"""
CLI Inv Custodias App
"""
import csv
from datetime import datetime
import time

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT, SLEEP

from .request_api import get_inv_custodias

encabezados = ["ID", "Usuario e-mail", "Nombre completo", "Distrito", "Edificio", "Oficina"]

app = typer.Typer()


@app.command()
def consultar(
    distrito_id: int = None,
    distrito_clave: str = None,
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
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
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
        table.add_row(
            str(registro["id"]),
            registro["usuario_email"],
            registro["nombre_completo"],
            registro["distrito_clave"],
            registro["domicilio_edificio"],
            registro["oficina_clave"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] custodias")


@app.command()
def guardar(
    distrito_id: int = None,
    distrito_clave: str = None,
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
                    distrito_id=distrito_id,
                    distrito_clave=distrito_clave,
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
                escritor.writerow(
                    [
                        registro["id"],
                        registro["usuario_email"],
                        registro["nombre_completo"],
                        registro["distrito_clave"],
                        registro["domicilio_edificio"],
                        registro["oficina_clave"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break
            rich.print(f"Van [green]{offset}[/green] custodias...")
            time.sleep(SLEEP)

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] custodias guardados en el archivo {nombre_archivo_csv}")
