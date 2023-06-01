"""
CLI Materias Tipos de Juicios Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_materias_tipos_juicios(
    materia_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar materias tipos de juicios"""
    parametros = {"limit": limit}
    if materia_id is not None:
        parametros["materia_id"] = materia_id
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/materias_tipos_juicios",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar materias tipos de juicios") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar materias tipos de juicios: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar materias tipos de juicios") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar materias tipos de juicios: " + datos["message"])
        raise CLIResponseError("Error al solicitar materias tipos de juicios")
    return datos["result"]
