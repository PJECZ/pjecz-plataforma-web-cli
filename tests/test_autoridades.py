"""
Unit tests for the autoridades
"""
import subprocess
import unittest


class TestAutoridades(unittest.TestCase):
    """Test autoridades"""

    def test_autoridades(self):
        """Test autoridades"""
        cmd = ["python3", "plataforma_web/app.py", "autoridades", "consultar"]
        try:
            result = subprocess.check_call(cmd)
        except subprocess.CalledProcessError as error:
            result = error.returncode
        self.assertEqual(result, 0)  # Check that exit code is 0
