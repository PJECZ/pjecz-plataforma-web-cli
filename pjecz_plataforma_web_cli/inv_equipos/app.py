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

encabezados = ["ID", "Custodia", "Usuario e-mail", "Nombre completo", "Distrito", "Oficina", "Marca", "Modelo", "Red", "F. Fab.", "No. Serie", "No. Inv.", "Tipo", "D. IP", "Mac Address", "Disco Duro", "Memoria", "Procesador"]

app = typer.Typer()


@app.command()
def consultar(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    distrito_id: int = None,
    distrito_clave: str = None,
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
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
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
        table.add_row(
            str(registro["id"]),
            str(registro["inv_custodia_id"]),
            registro["usuario_email"],
            registro["inv_custodia_nombre_completo"],
            registro["distrito_clave"],
            registro["oficina_clave"],
            registro["inv_marca_nombre"],
            registro["inv_modelo_descripcion"],
            registro["inv_red_nombre"],
            registro["fecha_fabricacion"],
            registro["numero_serie"],
            "" if registro["numero_inventario"] is None else str(registro["numero_inventario"]),
            registro["tipo"],
            registro["direccion_ip"],
            registro["direccion_mac"],
            registro["disco_duro"],
            registro["memoria_ram"],
            registro["procesador"],
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
                escritor.writerow(
                    [
                        registro["id"],
                        registro["inv_custodia_id"],
                        registro["usuario_email"],
                        registro["inv_custodia_nombre_completo"],
                        registro["distrito_clave"],
                        registro["oficina_clave"],
                        registro["inv_marca_nombre"],
                        registro["inv_modelo_descripcion"],
                        registro["inv_red_nombre"],
                        registro["fecha_fabricacion"],
                        registro["numero_serie"],
                        "" if registro["numero_inventario"] is None else str(registro["numero_inventario"]),
                        registro["tipo"],
                        registro["direccion_ip"],
                        registro["direccion_mac"],
                        registro["disco_duro"],
                        registro["memoria_ram"],
                        registro["procesador"],
                    ]
                )
            offset += LIMIT
            if offset >= respuesta["total"]:
                break

    # Mensaje de termino
    rich.print(f"Total: [green]{respuesta['total']}[/green] equipos guardados en el archivo {nombre_archivo_csv}")
