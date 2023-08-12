"""
CLI SIGA Salas App
"""
import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Clave", "Distrito", "Edificio", "Direccion IP", "Direccion NVR", "Estado"]

app = typer.Typer()


@app.command()
def consultar(
    distrito_id: int = None,
    distrito_clave: str = None,
    domicilio_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar salas"""
    rich.print("Consultar salas...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    if distrito_clave is not None:
        parametros["distrito_clave"] = distrito_clave
    if domicilio_id is not None:
        parametros["domicilio_id"] = domicilio_id
    try:
        respuesta = requests_get(
            subdirectorio="siga_grabaciones",
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
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["distrito_clave"],
            registro["domicilio_edificio"],
            registro["direccion_ip"],
            registro["direccion_nvr"],
            registro["estado"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] salas")
