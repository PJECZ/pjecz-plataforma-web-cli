"""
Config Settings
"""

import os

import pytz
from dotenv import load_dotenv

load_dotenv()

# Plataforma Web API key
API_HOST = os.getenv("API_HOST", "")
API_URL = API_HOST + "/v4"
API_KEY = os.getenv("API_KEY", "")

# Citas V2 API key
CITAS_V2_API_HOST = os.getenv("CITAS_V2_API_HOST", "")
CITAS_V2_API_URL = ""
if CITAS_V2_API_HOST != "":
    CITAS_V2_API_URL = CITAS_V2_API_HOST + "/v3"
CITAS_V2_API_KEY = os.getenv("CITAS_V2_API_KEY", "")

# Parametros limit, timeout y sleep en segundos
LIMIT = int(os.getenv("LIMIT", "40"))
TIMEOUT = int(os.getenv("TIMEOUT", "12"))
SLEEP = int(os.getenv("SLEEP", "4"))

# SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "")

# Huso horario
LOCAL_HUSO_HORARIO = pytz.timezone("America/Mexico_City")
SERVIDOR_HUSO_HORARIO = pytz.utc

# SIGA Justicia Ruta
SIGA_JUSTICIA_RUTA = os.getenv("SIGA_JUSTICIA_RUTA", "")
