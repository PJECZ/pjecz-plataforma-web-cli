"""
CLI Oficinas Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_oficinas(
    distrito_id: int = None,
    distrito_clave: str = None,
    domicilio_id: int = None,
    es_jurisdiccional: bool = None,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar oficinas"""
    parametros = {"limit": limit}
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    if distrito_clave is not None:
        parametros["distrito_clave"] = distrito_clave
    if domicilio_id is not None:
        parametros["domicilio_id"] = domicilio_id
    if es_jurisdiccional is not None:
        parametros["es_jurisdiccional"] = es_jurisdiccional
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/oficinas",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar oficinas") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar oficinas: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar oficinas") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar oficinas: " + datos["message"])
        raise CLIResponseError("Error al solicitar oficinas")
    return datos["result"]
