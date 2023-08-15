"""
CLI Materias App
"""
import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

app = typer.Typer()


@app.command()
def consultar(
    en_sentencias: bool = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar materias"""
    rich.print("Consultar materias...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if en_sentencias is not None:
        parametros["en_sentencias"] = en_sentencias
    try:
        respuesta = requests_get(
            subdirectorio="materias",
            parametros=parametros,
        )
    except MyAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table("ID", "Clave", "Nombre", "En sentencias")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["nombre"],
            "SI" if registro["en_sentencias"] else "",
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] materias")
