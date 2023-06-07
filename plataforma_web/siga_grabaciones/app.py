"""
CLI SIGA Grabaciones App
"""
from datetime import datetime, timedelta
from pathlib import Path
import os
import subprocess

import rich
import typer

from common.exceptions import CLIAnyError
from config.settings import LIMIT, SIGA_JUSTICIA_RUTA

from .request_api import get_siga_grabaciones, post_siga_grabacion

encabezados = ["ID", "Inicio", "Sala", "Autoridad", "Expediente", "Duración", "Tamaño"]

app = typer.Typer()


@app.command()
def consultar(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    materia_id: int = None,
    materia_clave: str = None,
    siga_sala_id: int = None,
    siga_sala_clave: str = None,
    limit: int = LIMIT,
    offset: int = 0,
):
    """Consultar grabaciones"""
    rich.print("Consultar grabaciones...")

    # Solicitar datos
    try:
        respuesta = get_siga_grabaciones(
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            materia_id=materia_id,
            materia_clave=materia_clave,
            siga_sala_id=siga_sala_id,
            siga_sala_clave=siga_sala_clave,
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
        inicio = datetime.strptime(registro["inicio"], "%Y-%m-%dT%H:%M:%S")
        duracion = timedelta(seconds=registro["duracion"])
        duracion_str = str(duracion).split(".")[0]
        tamanio = f"{registro['tamanio'] / (1024 * 1024):0.2f} MB"
        table.add_row(
            str(registro["id"]),
            inicio.strftime("%Y-%m-%d %H:%M:%S"),
            registro["siga_sala_clave"],
            registro["autoridad_clave"],
            registro["expediente"],
            duracion_str,
            tamanio,
        )
    console.print(table)

    # Mostrar el total
    rich.print(f"Total: [green]{respuesta['total']}[/green] grabaciones")


@app.command()
def crear(
    archivo_ruta: str,
):
    """Crea un nuevo registro de grabación"""
    rich.print("[bold cyan]=== Crear registro de grabación ===[/bold cyan]")

    # Extraer nombre del archivo
    archivo_nombre = os.path.basename(archivo_ruta)
    archivo_nombre = os.path.splitext(archivo_nombre)[0]

    # Revisar los pares de archivos .mp4 y .flv
    ruta = os.path.dirname(archivo_ruta)
    archivo_mp4_ruta = os.path.splitext(archivo_ruta)[0] + ".mp4"
    if not os.path.isfile(archivo_mp4_ruta):
        typer.secho("No se encuentra el archivo con extensión MP4", fg=typer.colors.RED)
        raise typer.Exit()
    archivo_flv_ruta = os.path.splitext(archivo_ruta)[0] + ".flv"
    if not os.path.isfile(archivo_flv_ruta):
        typer.secho("No se encuentra el archivo con extensión FLV", fg=typer.colors.RED)
        raise typer.Exit()

    # Extraer valores del nombre del archivo
    count_guion_bajos = archivo_nombre.count("_")
    if count_guion_bajos < 5:
        typer.secho("Error en el nombre del archivo. Falta de secciones separados por guiones bajos '_'.", fg=typer.colors.RED)
        raise typer.Exit()
    rich.print("[cyan]- Lectura de datos.[/cyan]")
    # Leer tiempo de inicio
    try:
        inicio_str = archivo_nombre.split("_")[0] + archivo_nombre.split("_")[1]
        inicio_datetime = datetime.strptime(inicio_str, "%Y%m%d%H%M%S")
        inicio_str = inicio_datetime.strftime("%Y/%m/%d %H:%M:%S")
    except:
        typer.secho("Error al leer la fecha-hora de inicio en el nombre del archivo. Formato no válido", fg=typer.colors.RED)
        raise typer.Exit()
    # Cálculos de tiempos
    # Extraer la duración del archivo de video mp4
    duracion = timedelta(seconds=4556.299)
    # try:
    #     process = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", archivo_mp4_ruta], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #     duracion = timedelta(seconds=float(process.stdout))
    # except:
    #     typer.secho("Error se necesita el programa 'ffprobe' para calcular la duración del video.", fg=typer.colors.RED)
    #     raise typer.Exit()
    termino_datetime = inicio_datetime + duracion
    termino_str = termino_datetime.strftime("%Y/%m/%d %H:%M:%S")
    # Extraer el tamaño del archivo
    tamanio = os.path.getsize(archivo_mp4_ruta)
    tamanio_str = f"{tamanio / (1024 * 1024):0.2f} MB"
    # Leer la Sala
    siga_sala_clave = archivo_nombre.split("_")[2]
    autoridad_clave = archivo_nombre.split("_")[3]
    materia_clave = archivo_nombre.split("_")[4]
    expediente = archivo_nombre.split("_")[5]
    # Calcular ruta dentro de justicia
    anio = f"{inicio_datetime.year:04d}"
    mes = f"{inicio_datetime.month:02d}"
    dia = f"{inicio_datetime.day:02d}"
    justicia_ruta = f"{SIGA_JUSTICIA_RUTA}/{siga_sala_clave}/{anio}/{mes}/{dia}"

    # Mostrar Metadatos
    rich.print(f"Ruta: [yellow]{ruta}[/yellow]")
    rich.print(f"Nombre del archivo: [yellow]{archivo_nombre}[/yellow]")
    rich.print(f"Inicio: [yellow]{inicio_str}[/yellow]")
    rich.print(f"Termino: [yellow]{termino_str}[/yellow]")
    rich.print(f"Duración: [yellow]{duracion}[/yellow]")
    rich.print(f"Tamaño: [yellow]{tamanio_str}[/yellow]")
    rich.print(f"SIGA Sala Clave: [yellow]{siga_sala_clave}[/yellow]")
    rich.print(f"Autoridad Clave: [yellow]{autoridad_clave}[/yellow]")
    rich.print(f"Materia Clave: [yellow]{materia_clave}[/yellow]")
    rich.print(f"Expediente: [yellow]{expediente}[/yellow]")
    rich.print(f"Justicia Ruta: [yellow]{justicia_ruta}[/yellow]")

    # Enviar datos
    rich.print("[cyan]- Envío de información.[/cyan]")
    try:
        respuesta = post_siga_grabacion(
            autoridad_clave=autoridad_clave,
            siga_sala_clave=siga_sala_clave,
            materia_clave=materia_clave,
            expediente=expediente,
            inicio=inicio_datetime,
            termino=termino_datetime,
            archivo_nombre=archivo_nombre,
            justicia_ruta=justicia_ruta,
            tamanio=tamanio,
            duracion=duracion,
        )
    except CLIAnyError as error:
        typer.secho(str(error), fg=typer.colors.RED)
        raise typer.Exit()

    # Mostrar Respuesta
    rich.print("[cyan]- Respuesta.[/cyan]")
    if respuesta["success"]:
        rich.print(f"[bold green]Registro Correcto. {respuesta['message']}[/bold green]")
        rich.print(f"ID registrado: [green]{respuesta['id']}[/green]")
    else:
        rich.print(f"[bold red]Registro Incorrecto. {respuesta['message']}[/bold red]")
