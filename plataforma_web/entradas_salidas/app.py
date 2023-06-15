"""
CLI Entradas-Salidas App
"""
import csv
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_entradas_salidas

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

    # Solicitar datos
    try:
        respuesta = get_entradas_salidas(
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
