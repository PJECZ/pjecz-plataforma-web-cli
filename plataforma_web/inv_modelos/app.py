"""
CLI Inv Modelos App
"""
import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

app = typer.Typer()


@app.command()
def consultar(
    inv_marca_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar modelos"""
    rich.print("Consultar modelos...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if inv_marca_id is not None:
        parametros["inv_marca_id"] = inv_marca_id
    try:
        respuesta = requests_get(
            subdirectorio="inv_modelos",
            parametros=parametros,
        )
    except MyAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table("ID", "Marca", "Descripcion")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["inv_marca_nombre"],
            registro["descripcion"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] modelos")
