"""
CLI Autoridades App
"""
import csv
from datetime import datetime
import time

import rich
import typer

from config.settings import LIMIT, SLEEP
from lib.exceptions import MyAnyError
from lib.requests import requests_get

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

    # Consultar a la API
    parametros = {"limit": limit, "offset": offset}
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    if distrito_clave is not None:
        parametros["distrito_clave"] = distrito_clave
    if es_cemasc is not None:
        parametros["es_cemasc"] = es_cemasc
    if es_creador_glosas is not None:
        parametros["es_creador_glosas"] = es_creador_glosas
    if es_defensoria is not None:
        parametros["es_defensoria"] = es_defensoria
    if es_jurisdiccional is not None:
        parametros["es_jurisdiccional"] = es_jurisdiccional
    if es_notaria is not None:
        parametros["es_notaria"] = es_notaria
    try:
        respuesta = requests_get(
            subdirectorio="autoridades",
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
def guardar(
    distrito_id: int = None,
    distrito_clave: str = None,
    es_cemasc: bool = None,
    es_creador_glosas: bool = None,
    es_defensoria: bool = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
):
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
            parametros = {"limit": LIMIT, "offset": offset}
            if distrito_id is not None:
                parametros["distrito_id"] = distrito_id
            if distrito_clave is not None:
                parametros["distrito_clave"] = distrito_clave
            if es_cemasc is not None:
                parametros["es_cemasc"] = es_cemasc
            if es_creador_glosas is not None:
                parametros["es_creador_glosas"] = es_creador_glosas
            if es_defensoria is not None:
                parametros["es_defensoria"] = es_defensoria
            if es_jurisdiccional is not None:
                parametros["es_jurisdiccional"] = es_jurisdiccional
            if es_notaria is not None:
                parametros["es_notaria"] = es_notaria
            try:
                respuesta = requests_get(
                    subdirectorio="autoridades",
                    parametros=parametros,
                )
            except MyAnyError as error:
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
            rich.print(f"Van [green]{offset}[/green] autoridades...")
            time.sleep(SLEEP)

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] autoridades guardados en el archivo {nombre_archivo_csv}")
