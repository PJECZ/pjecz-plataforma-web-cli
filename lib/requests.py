"""
Requests
"""
from typing import Any

import requests

from config.settings import API_KEY, API_URL, TIMEOUT
from lib.exceptions import MyConnectionError, MyRequestError, MyResponseError, MyStatusCodeError


def requests_get(
    subdirectorio: str,
    plural: str = "",
    parametros: dict = None,
) -> Any:
    """Solicitar roles"""
    if plural == "":
        plural = subdirectorio
    try:
        respuesta = requests.get(
            f"{API_URL}/{subdirectorio}",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise MyConnectionError(f"No hubo respuesta al solicitar {plural}") from error
    except requests.exceptions.HTTPError as error:
        raise MyStatusCodeError(f"Status Code al solicitar {plural}: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise MyRequestError(f"Error inesperado al solicitar {plural}") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False:
        if "message" in datos:
            raise MyResponseError(f"Fallo al solicitar {plural}: " + datos["message"])
        raise MyResponseError(f"Fallo al solicitar {plural}")
    return datos
