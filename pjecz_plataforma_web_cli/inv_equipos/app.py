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

encabezados = ["ID", "Creado", "Custodia", "Marca", "Modelo", "Red", "F. Fab.", "No. Serie", "No. Inv.", "Tipo", "D. IP", "Mac Address"]

app = typer.Typer()


@app.command()
def consultar(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    fecha_fabricacion_desde: str = None,
    fecha_fabricacion_hasta: str = None,
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


@app.command()
def guardar(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    fecha_fabricacion_desde: str = None,
    fecha_fabricacion_hasta: str = None,
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    tipo: str = None,
):
    """Guardar equipos en un archivo CSV"""
    rich.print("Guardar equipos...")

    # Definir el nombre del archivo CSV
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo_csv = f"inv_equipos_{fecha_hora}.csv"

    # Guardar los datos en un archivo CSV haciendo bucle de consultas a la API
    with open(nombre_archivo_csv, "w", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        offset = 0
        while True:
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
                    limit=LIMIT,
                    offset=offset,
                )
            except CLIAnyError as error:
                typer.secho(str(error), fg=typer.colors.RED)
                raise typer.Exit()
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
            offset += LIMIT
            if offset >= respuesta["total"]:
                break

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] equipos guardados en el archivo {nombre_archivo_csv}")
