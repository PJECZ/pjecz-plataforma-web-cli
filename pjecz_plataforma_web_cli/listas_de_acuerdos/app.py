"""
CLI Listas de Acuerdos App
"""
import csv
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_listas_de_acuerdos, get_listas_de_acuerdos_sintetizar_por_creado
from .send_messages import send_creadas

encabezados = ["ID", "Creado", "Autoridad", "Fecha", "Descripcion", "Archivo"]

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    fecha: str = None,
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar listas de acuerdos"""
    rich.print("Consultar listas de acuerdos...")

    # Solicitar datos
    try:
        respuesta = get_listas_de_acuerdos(
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
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
            registro["archivo"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] listas de acuerdos")


@app.command()
def guardar():
    """Guardar listas de acuerdos en un archivo CSV"""
    rich.print("Guardar listas de acuerdos...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"listas_de_acuerdos_{fecha_hora}.csv"

    # Guardar los datos en un archivo CSV haciendo bucle de consultas a la API
    with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        offset = 0
        while True:
            try:
                respuesta = get_listas_de_acuerdos(
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
                        registro["archivo"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] listas de acuerdos guardados en el archivo {nombre_archivo_csv}")


@app.command()
def consultar_creadas(
    creado: str,
    distrito_id: int = None,
    size: int = LIMIT,
):
    """Consultar listas de acuerdos sintetizados por creado"""
    rich.print("Consultar listas de acuerdos sintetizados por creado")
    try:
        respuesta = get_listas_de_acuerdos_sintetizar_por_creado(
            creado=creado,
            distrito_id=distrito_id,
            size=size,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("A. Clave", "Distrito", "Autoridad", "ID", "Fecha", "Creado", "Archivo")
    contador = 0
    for registro in respuesta["items"]:
        if registro["id"] == 0:
            table.add_row(
                registro["autoridad_clave"],
                registro["distrito_nombre_corto"],
                registro["autoridad_descripcion_corta"],
                "ND",
                "ND",
                "ND",
                "ND",
            )
            continue
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f%z")  # %z: UTC offset in the form +HHMM or -HHMM (empty string if the object is naive).
        table.add_row(
            registro["autoridad_clave"],
            registro["distrito_nombre_corto"],
            registro["autoridad_descripcion_corta"],
            str(registro["id"]),
            registro["fecha"],
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["archivo"],
        )
        contador += 1
    console.print(table)


@app.command()
def enviar_creadas(
    creado: str,
    email: str,
    size: int = LIMIT,
    test: bool = True,
):
    """Enviar listas de acuerdos sintetizados por creado"""
    rich.print("Enviar listas de acuerdos sintetizados por creado")
    try:
        mensaje = send_creadas(
            creado=creado,
            email=email,
            size=size,
            test=test,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    rich.print(mensaje)
