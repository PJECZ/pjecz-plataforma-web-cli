"""
CLI Listas de Acuerdos Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_listas_de_acuerdos(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    fecha: str = None,
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar listas de acuerdos"""
    parametros = {"limit": limit}
    if autoridad_id is not None:
        parametros["autoridad_id"] = autoridad_id
    if autoridad_clave is not None:
        parametros["autoridad_clave"] = autoridad_clave
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    if fecha is not None:
        parametros["fecha"] = fecha
    if fecha_desde is not None:
        parametros["fecha_desde"] = fecha_desde
    if fecha_hasta is not None:
        parametros["fecha_hasta"] = fecha_hasta
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/listas_de_acuerdos",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar listas de acuerdos") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar listas de acuerdos: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar listas de acuerdos") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar listas de acuerdos: " + datos["message"])
        raise CLIResponseError("Error al solicitar listas de acuerdos")
    return datos["result"]


def get_listas_de_acuerdos_sintetizar_por_creado(
    creado: str,
    distrito_id: int = None,
    size: int = LIMIT,
) -> Any:
    """Solicitar listas de acuerdos sintetizados por creado"""
    parametros = {"size": size}
    if creado is not None:
        parametros["creado"] = creado
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    try:
        respuesta = requests.get(
            f"{BASE_URL}/listas_de_acuerdos/sintetizar_por_creado",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar listas de acuerdos sintetizados por creado") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar listas de acuerdos sintetizados por creado: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar listas de acuerdos sintetizados por creado") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar listas de acuerdos sintetizados por creado: " + datos["message"])
        raise CLIResponseError("Error al solicitar listas de acuerdos sintetizados por creado")
    return datos["result"]
