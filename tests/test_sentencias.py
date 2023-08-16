"""
Unit tests for sentencias
"""
import os
import subprocess
import unittest

from dotenv import load_dotenv

load_dotenv()


class TestSentencias(unittest.TestCase):
    """Test sentencias"""

    autoriadad_clave = os.getenv("AUTORIDAD_CLAVE")

    def test_sentencias(self):
        """Test sentencias"""
        cmd = ["python3", "plataforma_web/app.py", "sentencias", "consultar", "--autoridad-clave", self.autoriadad_clave]
        try:
            result = subprocess.check_call(cmd)
        except subprocess.CalledProcessError as error:
            result = error.returncode
        self.assertEqual(result, 0)  # Check that exit code is 0
