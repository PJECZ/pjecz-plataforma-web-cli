"""
CLI Citas Dias Inhabiles App
"""
from datetime import date

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_cit_dias_inhabiles, get_citas_v2_cit_dias_inhabiles, post_cit_dia_inhabil

encabezados = ["ID", "Fecha", "Descripcion"]

app = typer.Typer()


@app.command()
def consultar(
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar dias inhabiles"""
    rich.print("Consultar dias inhabiles...")

    # Solicitar datos
    try:
        respuesta = get_cit_dias_inhabiles(
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
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
            registro["fecha"],
            registro["descripcion"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] dias inhabiles")


@app.command()
def sincronizar(
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
):
    """Sincronizar dias inhabiles con Citas V2"""
    rich.print("Sincronizar dias inhabiles con Citas V2...")

    # Si la fecha_desde es None, asignar la fecha actual
    if fecha_desde is None:
        fecha_desde = date.today().strftime("%Y-%m-%d")
    rich.print(f"Desde:        [green]{fecha_desde}[/green]")

    # Inicializar el offset y el total para hacer varias consultas
    offset = 0
    total = None
    contador = 0

    # Bucle para hacer varias consultas
    while total is None or offset < total:
        # Consultar datos a Citas V2
        try:
            datos = get_citas_v2_cit_dias_inhabiles(
                fecha_desde=fecha_desde,
                fecha_hasta=fecha_hasta,
                limit=limit,
                offset=offset,
            )
        except CLIAnyError as error:
            typer.secho(str(error), fg=typer.colors.RED)
            raise typer.Exit()

        # Si aun no se conoce el total, asignarlo
        if total is None:
            total = datos["total"]
            rich.print(f"Consultados:  [green]{total}[/green] dias inhabiles en Citas V2")

        # Crear los registros de los dias inhabiles que no existan
        for dato in datos["items"]:
            try:
                respuesta = post_cit_dia_inhabil(
                    fecha=dato["fecha"],
                    descripcion=dato["descripcion"],
                )
            except CLIAnyError as error:
                typer.secho(str(error), fg=typer.colors.RED)
                raise typer.Exit()
            if respuesta["success"] is False:
                rich.print(f"Omitido:      [yellow]{dato['fecha']}[/yellow] [red]{respuesta['message']}[/red]")
            else:
                contador += 1
                rich.print(f"Sincronizado: [green]{respuesta['fecha']}[/green] [blue]{respuesta['message']}[/blue]")

        # Incrementar el offset
        offset += limit

    # Mostrar el total de dias inhabiles creados
    rich.print(f"Total:        [green]{contador}[/green] dias inhabiles creados")
