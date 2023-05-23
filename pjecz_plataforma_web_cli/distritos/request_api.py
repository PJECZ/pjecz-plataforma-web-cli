"""
CLI Distritos Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_distritos(
    es_distrito: bool = None,
    es_distrito_judicial: bool = None,
    es_jurisdiccional: bool = None,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar distritos"""
    parametros = {"limit": limit}
    if es_distrito is not None:
        parametros["es_distrito"] = es_distrito
    if es_distrito_judicial is not None:
        parametros["es_distrito_judicial"] = es_distrito_judicial
    if es_jurisdiccional is not None:
        parametros["es_jurisdiccional"] = es_jurisdiccional
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/distritos",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar distritos") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar distritos: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar distritos") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar distritos: " + datos["message"])
        raise CLIResponseError("Error al solicitar distritos")
    return datos["result"]
