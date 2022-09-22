"""
CLI Autoridades Request API
"""
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIRequestError, CLIResponseError, CLIStatusCodeError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_autoridades(
    distrito_id: int = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    limit: int = LIMIT,
    materia_id: int = None,
    offset: int = 0,
    organo_jurisdiccional: str = None,
) -> Any:
    """Solicitar autoridades"""
    parametros = {"limit": limit}
    if distrito_id is not None:
        parametros["distrito_id"] = distrito_id
    if es_jurisdiccional is not None:
        parametros["es_jurisdiccional"] = es_jurisdiccional
    if es_notaria is not None:
        parametros["es_notaria"] = es_notaria
    if materia_id is not None:
        parametros["materia_id"] = materia_id
    if offset > 0:
        parametros["offset"] = offset
    if organo_jurisdiccional is not None:
        parametros["organo_jurisdiccional"] = organo_jurisdiccional
    try:
        respuesta = requests.get(
            f"{BASE_URL}/autoridades",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIConnectionError("No hubo respuesta al solicitar autoridades") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar autoridades: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIRequestError("Error inesperado al solicitar autoridades") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar autoridades: " + datos["message"])
        raise CLIResponseError("Error al solicitar autoridades")
    return datos["result"]
