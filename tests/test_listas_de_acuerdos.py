"""
Unit tests for listas de acuerdos
"""
import os
import subprocess
import unittest

from dotenv import load_dotenv

load_dotenv()


class TestListasDeAcuerdos(unittest.TestCase):
    """Test listas de acuerdos"""

    autoridad_clave = os.getenv("AUTORIDAD_CLAVE")

    def test_listas_de_acuerdos(self):
        """Test listas de acuerdos"""
        cmd = ["python3", "plataforma_web/app.py", "listas_de_acuerdos", "consultar", "--autoridad-clave", self.autoridad_clave]
        try:
            result = subprocess.check_call(cmd)
        except subprocess.CalledProcessError as error:
            result = error.returncode
        self.assertEqual(result, 0)
