"""
CLI SIGA Salas App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_siga_salas

encabezados = ["ID", "Clave", "Edificio", "Estado", "Dir. IP", "Dir. NVR"]

app = typer.Typer()


@app.command()
def consultar(
    distrito_id: int = None,
    distrito_clave: str = None,
    domicilio_id: int = None,
    estado: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar salas"""
    rich.print("Consultar salas...")

    # Solicitar datos
    try:
        respuesta = get_siga_salas(
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            domicilio_id=domicilio_id,
            estado=estado,
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
            registro["clave"],
            registro["domicilio_edificio"],
            registro["estado"],
            registro["direccion_ip"],
            registro["direccion_nvr"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] salas")
