"""
CLI Boletines App
"""
from datetime import datetime

import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Envío", "Asunto", "Puntero", "Término"]

app = typer.Typer()


@app.command()
def consultar(
    estado: str = None,
    envio_programado_desde: str = None,
    envio_programado_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar boletines"""
    rich.print("Consultar boletines...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if estado is not None:
        parametros["estado"] = estado
    if envio_programado_desde is not None:
        parametros["envio_programado_desde"] = envio_programado_desde
    if envio_programado_hasta is not None:
        parametros["envio_programado_hasta"] = envio_programado_hasta
    try:
        respuesta = requests_get(
            subdirectorio="boletines",
            parametros=parametros,
        )
    except MyAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for enca in encabezados:
        table.add_column(enca)
    for registro in respuesta["items"]:
        envio_programado_datetime = datetime.fromisoformat(registro["envio_programado"].replace("Z", "+00:00"))
        if registro["termino_programado"] is None:
            termino_programado_datetime = None
        else:
            termino_programado_datetime = datetime.fromisoformat(registro["termino_programado"].replace("Z", "+00:00"))
        table.add_row(
            str(registro["id"]),
            envio_programado_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            registro["asunto"],
            str(registro["puntero"]),
            "ND" if termino_programado_datetime is None else termino_programado_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] boletines")
