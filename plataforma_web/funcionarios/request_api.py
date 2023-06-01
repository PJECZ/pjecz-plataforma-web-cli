"""
CLI Funcionarios Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_funcionarios(
    en_funciones: bool = None,
    en_soportes: bool = None,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar funcionarios"""
    parametros = {"limit": limit}
    if en_funciones is not None:
        parametros["en_funciones"] = en_funciones
    if en_soportes is not None:
        parametros["en_soportes"] = en_soportes
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/funcionarios",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar funcionarios") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar funcionarios: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar funcionarios") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar funcionarios: " + datos["message"])
        raise CLIResponseError("Error al solicitar funcionarios")
    return datos["result"]
