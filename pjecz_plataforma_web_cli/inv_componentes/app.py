"""
CLI Inv Componentes App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_inv_componentes

app = typer.Typer()


@app.command()
def consultar(
    generacion: str = None,
    inv_categoria_id: int = None,
    inv_equipo_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar componentes"""
    rich.print("Consultar componentes...")
    try:
        respuesta = get_inv_componentes(
            generacion=generacion,
            inv_categoria_id=inv_categoria_id,
            inv_equipo_id=inv_equipo_id,
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Categoria", "Equipo ID", "Equipo Desc.", "Descripcion", "Cantidad", "Generacion", "Version")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["inv_categoria_nombre"],
            str(registro["inv_equipo_id"]),
            registro["inv_equipo_descripcion"],
            registro["descripcion"],
            str(registro["cantidad"]),
            registro["generacion"],
            registro["version"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] componentes")
