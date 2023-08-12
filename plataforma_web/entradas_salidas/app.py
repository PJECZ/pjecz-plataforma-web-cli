"""
CLI Entradas-Salidas App
"""
from datetime import datetime

import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Creado", "email", "Tipo", "Direccion IP"]

app = typer.Typer()


@app.command()
def consultar(
    usuario_id: int = None,
    usuario_email: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar entradas-salidas"""
    rich.print("Consultar entradas-salidas...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if usuario_id is not None:
        parametros["usuario_id"] = usuario_id
    if usuario_email is not None:
        parametros["usuario_email"] = usuario_email
    try:
        respuesta = requests_get(
            subdirectorio="entradas_salidas",
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
        creado_datetime = datetime.fromisoformat(registro["creado"].replace("Z", "+00:00"))
        table.add_row(
            str(registro["id"]),
            creado_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            registro["usuario_email"],
            registro["tipo"],
            registro["direccion_ip"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] entradas-salidas")
