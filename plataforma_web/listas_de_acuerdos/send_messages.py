"""
CLI Listas de Acuerdos Send Messages
"""
from datetime import datetime
import locale
from pathlib import Path
from typing import Any

from dominate import document
from dominate.tags import div
from dominate.util import raw
import pandas as pd
import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail
from tabulate import tabulate

from common.exceptions import CLIConfigurationError, CLIAnyError, CLINoDataWarning
from config.settings import LIMIT, SENDGRID_API_KEY, SENDGRID_FROM_EMAIL

from .request_api import get_listas_de_acuerdos_sintetizar_por_creado

# Pandas options on how to display dataframes
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 150)

# Region
locale.setlocale(locale.LC_TIME, "es_MX.utf8")


def send_creadas(
    creado: str,
    email: str,
    size: int = LIMIT,
    test: bool = True,
) -> Any:
    """Enviar listas de acuerdos sintetizados por creado"""

    # Si test es falso, entonces se va a usar SendGrid
    sendgrid_client = None
    from_email = None
    if test is False:
        # Validar variables de entorno
        if SENDGRID_API_KEY == "":
            raise CLIConfigurationError("Falta SENDGRID_API_KEY")
        if SENDGRID_FROM_EMAIL == "":
            raise CLIConfigurationError("Falta SENDGRID_FROM_EMAIL")
        # Inicializar SendGrid
        sendgrid_client = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        from_email = Email(SENDGRID_FROM_EMAIL)

    # Solicitar datos a la API
    respuesta = get_listas_de_acuerdos_sintetizar_por_creado(
        creado=creado,
        size=size,
    )

    # Terminar si no hay resultados
    if respuesta["total"] == 0:
        raise CLINoDataWarning("No hay resultados al solicitar acuerdos sintetizados por creado")

    # Definir el asunto
    asunto = f"Listas de acuerdos creadas el {creado}"

    # Definir encabezados y renglones de la tabla
    encabezados = ["A. Clave", "Distrito", "Autoridad", "ID", "Fecha", "Creado", "Archivo"]
    renglones = []
    for dato in respuesta["items"]:
        if dato["id"] == 0:
            renglones.append(
                [
                    dato["autoridad_clave"],
                    dato["distrito_nombre_corto"],
                    dato["autoridad_descripcion_corta"],
                    "ND",
                    "ND",
                    "ND",
                    "ND",
                ]
            )
            continue
        dato_creado = datetime.strptime(dato["creado"], "%Y-%m-%dT%H:%M:%S.%f%z")  # %z: UTC offset in the form +HHMM or -HHMM (empty string if the object is naive).
        renglones.append(
            [
                dato["autoridad_clave"],
                dato["distrito_nombre_corto"],
                dato["autoridad_descripcion_corta"],
                dato["id"],
                dato["fecha"],
                dato_creado.strftime("%Y-%m-%d %H:%M:%S"),
                dato["archivo"] if test else f"<a href=\"{dato['url']}\">{dato['archivo']}</a>",
            ]
        )

    # Crear tabla HTML
    tabla_html = tabulate(renglones, headers=encabezados, tablefmt="unsafehtml")
    tabla_html = tabla_html.replace("<table>", '<table border="1" style="width:100%; border: 1px solid black; border-collapse: collapse;">')
    tabla_html = tabla_html.replace('<td style="', '<td style="padding: 4px;')
    tabla_html = tabla_html.replace("<td>", '<td style="padding: 4px;">')

    # Crear el cuerpo del mensaje
    elaboracion_fecha_hora_str = datetime.now().strftime("%d/%B/%Y %I:%M%p")
    contenidos = []
    contenidos.append("<style> td {border:2px black solid !important} </style>")
    contenidos.append("<h1>PJECZ Plataforma Web</h1>")
    contenidos.append(f"<h2>{asunto}</h2>")
    contenidos.append(tabla_html)
    contenidos.append(f"<p>Fecha de elaboración: <b>{elaboracion_fecha_hora_str}.</b></p>")
    contenidos.append("<p>ESTE MENSAJE ES ELABORADO POR UN PROGRAMA. FAVOR DE NO RESPONDER.</p>")

    # Si NO es una prueba, enviar mensaje
    if test is False:
        to_email = To(email)
        content = Content("text/html", "<br>".join(contenidos))
        mail = Mail(from_email=from_email, to_emails=to_email, subject=asunto, html_content=content)
        try:
            sendgrid_client.client.mail.send.post(request_body=mail.get())
        except Exception as error:
            raise CLIAnyError(str(error))
        return f"Mensaje enviado a {email} con {asunto}"

    # Es una prueba, entonces se va a guardar como un archivo HTML
    with document(title=asunto) as doc:
        for contenido in contenidos:
            div(raw(contenido))
    archivo = f"listas-de-acuerdos-enviar-creadas-{creado}.html"
    ruta = Path(archivo)
    with open(ruta, "w", encoding="utf-8") as puntero:
        puntero.write(doc.render())

    # Entregar mensaje
    return f"Se guardo {archivo} con {asunto} porque esta en modo de pruebas"
