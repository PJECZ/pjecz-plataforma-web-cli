"""
CLI Materias Tipos de Juicios App
"""
import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

app = typer.Typer()


@app.command()
def consultar(
    materia_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar tipos de juicios"""
    rich.print("Consultar tipos de juicios...")

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if materia_id is not None:
        parametros["materia_id"] = materia_id
    try:
        respuesta = requests_get(
            subdirectorio="materias_tipos_juicios",
            parametros=parametros,
        )
    except MyAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table("ID", "Materia", "Descripcion")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["materia_nombre"],
            registro["descripcion"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] tipos de juicios")
