"""
CLI Usuarios App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_usuarios

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    limit: int = LIMIT,
    oficina_id: int = None,
    oficina_clave: str = None,
    offset: int = 0,
):
    """Consultar usuarios"""
    rich.print("Consultar usuarios...")
    try:
        respuesta = get_usuarios(
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            limit=limit,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Distrito", "Autoridad", "Oficina", "email", "Nombres", "A. Paterno", "A. Materno")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["distrito_nombre_corto"],
            registro["autoridad_descripcion_corta"],
            registro["oficina_clave"],
            registro["email"],
            registro["nombres"],
            registro["apellido_paterno"],
            registro["apellido_materno"],
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] usuarios")
