"""
CLI Inv Equipos App
"""
import csv
from datetime import datetime

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT

from .request_api import get_inv_equipos

app = typer.Typer()


@app.command()
def consultar(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    fecha_fabricacion_desde: str = None,
    fecha_fabricacion_hasta: str = None,
    guardar: bool = False,
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    tipo: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar equipos"""
    rich.print("Consultar equipos...")

    # Solicitar datos
    try:
        respuesta = get_inv_equipos(
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            fecha_fabricacion_desde=fecha_fabricacion_desde,
            fecha_fabricacion_hasta=fecha_fabricacion_hasta,
            inv_custodia_id=inv_custodia_id,
            inv_modelo_id=inv_modelo_id,
            inv_red_id=inv_red_id,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            tipo=tipo,
            limit=limit,
            offset=offset,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Encabezados
    encabezados = ["ID", "Creado", "Custodia", "Marca", "Modelo", "Red", "F. Fab.", "No. S.", "No. I.", "Tipo", "D. IP", "M. A."]

    # Guardar datos en un archivo CSV
    if guardar:
        fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo_csv = f"inv_equipos_{fecha_hora}.csv"
        with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezados)
            for registro in respuesta["items"]:
                creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
                escritor.writerow(
                    [
                        registro["id"],
                        creado.strftime("%Y-%m-%d %H:%M:%S"),
                        registro["inv_custodia_id"],
                        registro["inv_marca_nombre"],
                        registro["inv_modelo_descripcion"],
                        registro["inv_red_nombre"],
                        registro["fecha_fabricacion"],
                        registro["numero_serie"],
                        "" if registro["numero_inventario"] is None else str(registro["numero_inventario"]),
                        registro["tipo"],
                        registro["direccion_ip"],
                        registro["direccion_mac"],
                    ]
                )
        rich.print(f"Datos guardados en el archivo {nombre_archivo_csv}")

    # Mostrar la tabla
    console = rich.console.Console()
    table = rich.table.Table()
    for enca in encabezados:
        table.add_column(enca)
    for registro in respuesta["items"]:
        creado = datetime.strptime(registro["creado"], "%Y-%m-%dT%H:%M:%S.%f")
        table.add_row(
            str(registro["id"]),
            creado.strftime("%Y-%m-%d %H:%M:%S"),
            str(registro["inv_custodia_id"]),
            registro["inv_marca_nombre"],
            registro["inv_modelo_descripcion"],
            registro["inv_red_nombre"],
            registro["fecha_fabricacion"],
            registro["numero_serie"],
            "" if registro["numero_inventario"] is None else str(registro["numero_inventario"]),
            registro["tipo"],
            registro["direccion_ip"],
            registro["direccion_mac"],
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] equipos")
