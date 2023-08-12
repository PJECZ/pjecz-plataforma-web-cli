"""
CLI Citas Dias Inhabiles App
"""
import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Fecha", "Descripcion"]

app = typer.Typer()


@app.command()
def consultar(
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar dias inhabiles"""
    rich.print("Consultar dias inhabiles...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if fecha_desde is not None:
        parametros["fecha_desde"] = fecha_desde
    if fecha_hasta is not None:
        parametros["fecha_hasta"] = fecha_hasta
    try:
        respuesta = requests_get(
            subdirectorio="cit_dias_inhabiles",
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
            registro["fecha"],
            registro["descripcion"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] dias inhabiles")
