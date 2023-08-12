"""
CLI Permisos App
"""
import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

app = typer.Typer()


@app.command()
def consultar(
    modulo_id: int = None,
    rol_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar permisos"""
    rich.print("Consultar permisos...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if modulo_id is not None:
        parametros["modulo_id"] = modulo_id
    if rol_id is not None:
        parametros["rol_id"] = rol_id
    try:
        respuesta = requests_get(
            subdirectorio="permisos",
            parametros=parametros,
        )
    except MyAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table("ID", "Rol", "Modulo", "Nivel")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["rol_nombre"],
            registro["modulo_nombre"],
            str(registro["nivel"]),
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] permisos")
