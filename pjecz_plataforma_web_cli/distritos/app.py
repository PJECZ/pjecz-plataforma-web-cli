"""
CLI Distritos App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_distritos

app = typer.Typer()


@app.command()
def consultar(
    es_distrito: bool = None,
    es_distrito_judicial: bool = None,
    es_jurisdiccional: bool = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar distritos"""
    rich.print("Consultar distritos...")
    try:
        respuesta = get_distritos(
            es_distrito=es_distrito,
            es_distrito_judicial=es_distrito_judicial,
            es_jurisdiccional=es_jurisdiccional,
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Clave", "Nombre", "Nombre Corto", "Es D.", "Es J.", "Es D.J.")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["nombre"],
            registro["nombre_corto"],
            "SI" if registro["es_distrito"] else "",
            "SI" if registro["es_jurisdiccional"] else "",
            "SI" if registro["es_distrito_judicial"] else "",
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] distritos")
