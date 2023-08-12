"""
CLI Funcionarios App
"""
import rich
import typer

from config.settings import LIMIT
from lib.exceptions import MyAnyError
from lib.requests import requests_get

encabezados = ["ID", "Nombres", "A. Paterno", "A. Materno", "CURP", "e-mail", "En F.", "En S."]

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

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if en_funciones is not None:
        parametros["en_funciones"] = en_funciones
    if en_soportes is not None:
        parametros["en_soportes"] = en_soportes
    try:
        respuesta = requests_get(
            subdirectorio="funcionarios",
            parametros=parametros,
        )
    except MyAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for enca in encabezados:
        table.add_column(enca)
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

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] funcionario")
