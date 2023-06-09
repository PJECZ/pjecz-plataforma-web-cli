"""
CLI SIGA Grabaciones Request API
"""
from typing import Any
from datetime import datetime, timedelta

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_siga_grabaciones(
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
) -> Any:
    """Solicitar grabaciones"""
    parametros = {"limit": limit}
    if offset > 0:
        parametros["offset"] = offset
    if autoridad_id is not None:
        parametros["autoridad_id"] = autoridad_id
    if autoridad_clave is not None:
        parametros["autoridad_clave"] = autoridad_clave
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    if distrito_clave is not None:
        parametros["distrito_clave"] = distrito_clave
    if materia_id is not None:
        parametros["materia_id"] = materia_id
    if materia_clave is not None:
        parametros["materia_clave"] = materia_clave
    if siga_sala_id is not None:
        parametros["siga_sala_id"] = siga_sala_id
    if siga_sala_clave is not None:
        parametros["siga_sala_clave"] = siga_sala_clave
    try:
        respuesta = requests.get(
            f"{BASE_URL}/siga_grabaciones",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar grabaciones") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar grabaciones: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar grabaciones") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar grabaciones: " + datos["message"])
        raise CLIResponseError("Error al solicitar grabaciones")
    return datos["result"]


def post_siga_grabacion(
    autoridad_clave: str,
    siga_sala_clave: str,
    materia_clave: str,
    expediente: str,
    inicio: datetime,
    termino: datetime,
    archivo_nombre: str,
    justicia_ruta: str,
    tamanio: int,
    duracion: timedelta,
) -> Any:
    """Enviar datos de una grabación"""
    parametros = {
        "autoridad_clave": autoridad_clave,
        "siga_sala_clave": siga_sala_clave,
        "materia_clave": materia_clave,
        "expediente": expediente,
        "inicio": str(inicio),
        "termino": str(termino),
        "archivo_nombre": archivo_nombre,
        "justicia_ruta": justicia_ruta,
        "tamanio": tamanio,
        "duracion": int(duracion.total_seconds()),
        "estado": "VALIDO",
    }
    try:
        respuesta = requests.post(
            f"{BASE_URL}/siga_grabaciones",
            headers={"X-Api-Key": API_KEY},
            json=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al crear la grabación") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al crear la grabación: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al crear la grabación") from error
    datos = respuesta.json()
    print(datos)
    if "success" not in datos or datos["success"] is False:
        if "message" in datos:
            raise CLIResponseError("Error al enviar grabación: " + datos["message"])
        raise CLIResponseError("Error al enviar grabación")
    return datos
