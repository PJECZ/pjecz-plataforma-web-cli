"""
CLI Inv Custodias App
"""
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_inv_custodias

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
    console = rich.console.Console()
    table = rich.table.Table("ID", "Creado", "Usuario", "Nombre completo")
    for registro in respuesta["items"]:
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            registro["usuario_email"],
            registro["nombre_completo"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] custodias")
