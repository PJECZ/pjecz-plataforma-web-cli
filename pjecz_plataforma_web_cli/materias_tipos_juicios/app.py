"""
CLI Materias Tipos de Juicios App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_materias_tipos_juicios

app = typer.Typer()


@app.command()
def consultar(
    limit: int = LIMIT,
    materia_id: int = None,
    offset: int = 0,
):
    """Consultar tipos de juicios"""
    rich.print("Consultar tipos de juicios...")
    try:
        respuesta = get_materias_tipos_juicios(
            limit=limit,
            materia_id=materia_id,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Materia", "Descripcion")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["materia_nombre"],
            registro["descripcion"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] tipos de juicios")
