"""
CLI Autoridades App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_autoridades

app = typer.Typer()


@app.command()
def consultar(
    distrito_id: int = None,
    distrito_clave: str = None,
    es_cemasc: bool = None,
    es_creador_glosas: bool = None,
    es_defensoria: bool = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar autoridades"""
    rich.print("Consultar autoridades...")
    try:
        respuesta = get_autoridades(
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            es_cemasc=es_cemasc,
            es_creador_glosas=es_creador_glosas,
            es_defensoria=es_defensoria,
            es_jurisdiccional=es_jurisdiccional,
            es_notaria=es_notaria,
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Clave", "Descripcion", "Distrito", "Materia", "Es J.", "Es N.", "Organo J.")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["descripcion_corta"],
            registro["distrito_nombre_corto"],
            registro["materia_nombre"],
            "SI" if registro["es_jurisdiccional"] else "NO",
            "SI" if registro["es_notaria"] else "NO",
            registro["organo_jurisdiccional"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] autoridades")
