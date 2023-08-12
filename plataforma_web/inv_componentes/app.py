"""
CLI Inv Componentes App
"""
import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Categoria", "Equipo ID", "Equipo Desc.", "Descripcion", "Cantidad", "Generacion", "Version"]

app = typer.Typer()


@app.command()
def consultar(
    generacion: str = None,
    inv_categoria_id: int = None,
    inv_equipo_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar componentes"""
    rich.print("Consultar componentes...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if generacion is not None:
        parametros["generacion"] = generacion
    if inv_categoria_id is not None:
        parametros["inv_categoria_id"] = inv_categoria_id
    if inv_equipo_id is not None:
        parametros["inv_equipo_id"] = inv_equipo_id
    try:
        respuesta = requests_get(
            subdirectorio="inv_componentes",
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
            registro["inv_categoria_nombre"],
            str(registro["inv_equipo_id"]),
            registro["inv_equipo_descripcion"],
            registro["descripcion"],
            str(registro["cantidad"]),
            registro["generacion"],
            registro["version"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] componentes")
