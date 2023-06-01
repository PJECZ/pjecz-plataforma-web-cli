"""
CLI Inv Componentes Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_inv_componentes(
    generacion: str = None,
    inv_categoria_id: int = None,
    inv_equipo_id: int = None,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar componentes"""
    parametros = {"limit": limit}
    if generacion is not None:
        parametros["generacion"] = generacion
    if inv_categoria_id is not None:
        parametros["inv_categoria_id"] = inv_categoria_id
    if inv_equipo_id is not None:
        parametros["inv_equipo_id"] = inv_equipo_id
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/inv_componentes",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar componentes") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar componentes: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar componentes") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar componentes: " + datos["message"])
        raise CLIResponseError("Error al solicitar componentes")
    return datos["result"]
