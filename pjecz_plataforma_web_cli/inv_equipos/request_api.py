"""
CLI Inv Equipos Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_inv_equipos(
    creado: str = None,
    creado_desde: str = None,
    creado_hasta: str = None,
    fecha_fabricacion_desde: str = None,
    fecha_fabricacion_hasta: str = None,
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    tipo: str = None,
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar equipos"""
    parametros = {"limit": limit}
    if creado is not None:
        parametros["creado"] = creado
    if creado_desde is not None:
        parametros["creado_desde"] = creado_desde
    if creado_hasta is not None:
        parametros["creado_hasta"] = creado_hasta
    if fecha_fabricacion_desde is not None:
        parametros["fecha_fabricacion"] = fecha_fabricacion_desde
    if fecha_fabricacion_hasta is not None:
        parametros["fecha_fabricacion"] = fecha_fabricacion_hasta
    if inv_custodia_id is not None:
        parametros["inv_custodia_id"] = inv_custodia_id
    if inv_modelo_id is not None:
        parametros["inv_modelo_id"] = inv_modelo_id
    if inv_red_id is not None:
        parametros["inv_red_id"] = inv_red_id
    if oficina_id is not None:
        parametros["oficina_id"] = oficina_id
    if oficina_clave is not None:
        parametros["oficina_clave"] = oficina_clave
    if tipo is not None:
        parametros["tipo"] = tipo
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/inv_equipos",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar equipos") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar equipos: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar equipos") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar equipos: " + datos["message"])
        raise CLIResponseError("Error al solicitar equipos")
    return datos["result"]
