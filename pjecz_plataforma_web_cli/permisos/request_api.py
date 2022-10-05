"""
CLI Permisos Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_permisos(
    modulo_id: int = None,
    rol_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar permisos"""
    parametros = {"limit": limit}
    if modulo_id is not None:
        parametros["modulo_id"] = modulo_id
    if rol_id is not None:
        parametros["rol_id"] = rol_id
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/permisos",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar permisos") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar permisos: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar permisos") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar permisos: " + datos["message"])
        raise CLIResponseError("Error al solicitar permisos")
    return datos["result"]
