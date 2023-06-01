"""
CLI Inv Custodias Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_inv_custodias(
    distrito_id: int = None,
    distrito_clave: str = None,
    fecha_desde: str = None,
    fecha_hasta: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar custodias"""
    parametros = {"limit": limit}
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    if distrito_clave is not None:
        parametros["distrito_clave"] = distrito_clave
    if fecha_desde is not None:
        parametros["fecha"] = fecha_desde
    if fecha_hasta is not None:
        parametros["fecha"] = fecha_hasta
    if usuario_id is not None:
        parametros["usuario_id"] = usuario_id
    if usuario_email is not None:
        parametros["usuario_email"] = usuario_email
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/inv_custodias",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar custodias") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar custodias: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar custodias") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar custodias: " + datos["message"])
        raise CLIResponseError("Error al solicitar custodias")
    return datos["result"]
