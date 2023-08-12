"""
CLI Centros de Trabajo App
"""
import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Clave", "Nombre", "Distrito", "Domicilio", "Telefono"]

app = typer.Typer()


@app.command()
def consultar(
    distrito_id: int = None,
    domicilio_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar centros de trabajo"""
    rich.print("Consultar centros de trabajo...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    if domicilio_id is not None:
        parametros["domicilio_id"] = domicilio_id
    try:
        respuesta = requests_get(
            subdirectorio="centros_trabajos",
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
            registro["nombre"],
            registro["distrito_nombre_corto"],
            registro["domicilio_completo"],
            registro["telefono"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] centros de trabajo")
