"""
CLI Funcionarios App
"""
import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_funcionarios

app = typer.Typer()


@app.command()
def consultar(
    en_funciones: bool = None,
    en_soportes: bool = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar funcionarios"""
    rich.print("Consultar funcionario...")
    try:
        respuesta = get_funcionarios(
            en_funciones=en_funciones,
            en_soportes=en_soportes,
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()
    console = rich.console.Console()
    table = rich.table.Table("ID", "Nombres", "A. Paterno", "A. Materno", "CURP", "e-mail", "En F.", "En S.")
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["nombres"],
            registro["apellido_paterno"],
            registro["apellido_materno"],
            registro["curp"],
            registro["email"],
            "SI" if registro["en_funciones"] else "NO",
            "SI" if registro["en_soportes"] else "NO",
        )
    console.print(table)
    rich.print(f"Total: [green]{respuesta['total']}[/green] funcionario")
