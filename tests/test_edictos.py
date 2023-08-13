"""
Unit tests for edictos
"""
import os
import subprocess
import unittest

from dotenv import load_dotenv

load_dotenv()


class TestEdictos(unittest.TestCase):
    """Test edictos"""

    autoridad_clave = os.getenv("AUTORIDAD_CLAVE")

    def test_edictos(self):
        """Test edictos"""
        cmd = ["python3", "plataforma_web/app.py", "edictos", "consultar", "--autoridad-clave", self.autoridad_clave]
        try:
            result = subprocess.check_call(cmd)
        except subprocess.CalledProcessError as error:
            result = error.returncode
        self.assertEqual(result, 0)  # Check that exit code is 0
