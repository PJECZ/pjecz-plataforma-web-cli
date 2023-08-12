"""
CLI Roles App
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
    """Consultar roles"""
    rich.print("Consultar roles...")

    # Consultar a la API
    try:
        respuesta = requests_get(
            subdirectorio="roles",
            parametros={"limit": limit, "offset": offset},
        )
    except MyAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table("ID", "Nombre")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["nombre"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] roles")
