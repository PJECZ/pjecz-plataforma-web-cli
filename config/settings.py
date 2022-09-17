"""
Config Settings
"""
import os

from dotenv import load_dotenv
import pytz

load_dotenv()

# Host and base URL
HOST = os.getenv("HOST", "")
BASE_URL = f"{HOST}/v2"

# Default limit and timeout in seconds
LIMIT = int(os.getenv("LIMIT", "40"))
TIMEOUT = int(os.getenv("TIMEOUT", "12"))

# Username and password
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")

# SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "")

# Huso horario local
LOCAL_HUSO_HORARIO = pytz.timezone("America/Mexico_City")
SERVIDOR_HUSO_HORARIO = pytz.utc
