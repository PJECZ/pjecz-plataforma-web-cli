"""
CLI Modulos App
"""
import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar modulos"""
    rich.print("Consultar modulos...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    try:
        respuesta = requests_get(
            subdirectorio="modulos",
            parametros=parametros,
        )
    except MyAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table("ID", "Nombre", "Nombre corto", "Icono", "Ruta", "En N.")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["nombre"],
            registro["nombre_corto"],
            registro["icono"],
            registro["ruta"],
            "SI" if registro["en_navegacion"] else "NO",
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] modulos")
