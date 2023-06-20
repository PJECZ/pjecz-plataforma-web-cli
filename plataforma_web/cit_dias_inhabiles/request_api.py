"""
CLI Citas Dias Inhabiles Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, CITAS_V2_BASE_URL, CITAS_V2_API_KEY, LIMIT, TIMEOUT


def get_cit_dias_inhabiles(
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
    base_url: str = BASE_URL,
    api_key: str = API_KEY,
) -> Any:
    """Solicitar dias inhabiles"""
    parametros = {"limit": limit}
    if fecha_desde is not None:
        parametros["fecha_desde"] = fecha_desde
    if fecha_hasta is not None:
        parametros["fecha_hasta"] = fecha_hasta
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            url=f"{base_url}/cit_dias_inhabiles",
            headers={"X-Api-Key": api_key},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar dias inhabiles") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar dias inhabiles: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar dias inhabiles") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar dias inhabiles: " + datos["message"])
        raise CLIResponseError("Error al solicitar dias inhabiles")
    return datos["result"]


def get_citas_v2_cit_dias_inhabiles(
    fecha_desde: str = None,
    fecha_hasta: str = None,
    limit: int = LIMIT,
    offset: int = 0,
    base_url: str = CITAS_V2_BASE_URL,
    api_key: str = CITAS_V2_API_KEY,
) -> Any:
    """Solicitar dias inhabiles a Citas V2"""
    return get_cit_dias_inhabiles(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        limit=limit,
        offset=offset,
        base_url=base_url,
        api_key=api_key,
    )


def post_cit_dia_inhabil(
    fecha: str,
    descripcion: str,
) -> Any:
    """Crear un dia inhabil"""
    parametros = {"fecha": fecha, "descripcion": descripcion}
    try:
        respuesta = requests.post(
            f"{BASE_URL}/cit_dias_inhabiles",
            headers={"X-Api-Key": API_KEY},
            json=parametros,
            timeout=TIMEOUT,
        )
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al crear la grabación") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al crear la grabación: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al crear la grabación") from error
    datos = respuesta.json()
    if "success" not in datos or "message" not in datos:
        raise CLIResponseError("Error porque falta success o message al crear la grabación")
    return datos
