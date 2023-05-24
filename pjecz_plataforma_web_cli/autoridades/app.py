"""
CLI Autoridades App
"""
import csv
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_autoridades

encabezados = ["ID", "Clave", "Desc. corta", "Distrito", "CEMASC", "Glosas", "Def.", "Es J.", "Es N.", "O.J."]

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

    # Solicitar datos
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

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for enca in encabezados:
        table.add_column(enca)
    for registro in respuesta["items"]:
        table.add_row(
            str(registro["id"]),
            registro["clave"],
            registro["descripcion_corta"],
            registro["distrito_nombre_corto"],
            "SI" if registro["es_cemasc"] else "",
            "SI" if registro["es_creador_glosas"] else "",
            "SI" if registro["es_defensoria"] else "",
            "SI" if registro["es_jurisdiccional"] else "",
            "SI" if registro["es_notaria"] else "",
            registro["organo_jurisdiccional"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] autoridades")


@app.command()
def guardar():
    """Guardar autoridades en un archivo CSV"""
    rich.print("Guardar autoridades...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"autoridades_{fecha_hora}.csv"

    # Guardar los datos en un archivo CSV haciendo bucle de consultas a la API
    with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        offset = 0
        while True:
            try:
                respuesta = get_autoridades(
                    limit=LIMIT,
                    offset=offset,
                )
            except CLIAnyError as error:
                typer.secho(str(error), fg=typer.colors.RED)
                raise typer.Exit()
            for registro in respuesta["items"]:
                escritor.writerow(
                    [
                        registro["id"],
                        registro["clave"],
                        registro["descripcion_corta"],
                        registro["distrito_nombre_corto"],
                        "SI" if registro["es_cemasc"] else "",
                        "SI" if registro["es_creador_glosas"] else "",
                        "SI" if registro["es_defensoria"] else "",
                        "SI" if registro["es_jurisdiccional"] else "",
                        "SI" if registro["es_notaria"] else "",
                        registro["organo_jurisdiccional"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] autoridades guardados en el archivo {nombre_archivo_csv}")
