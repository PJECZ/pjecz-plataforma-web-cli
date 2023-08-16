"""
Unit tests for distritos
"""
import subprocess
import unittest


class TestDistritos(unittest.TestCase):
    """Test distritos"""

    def test_distritos(self):
        """Test distritos"""
        cmd = ["python3", "plataforma_web/app.py", "distritos", "consultar"]
        try:
            result = subprocess.check_call(cmd)
        except subprocess.CalledProcessError as error:
            result = error.returncode
        self.assertEqual(result, 0)  # Check that exit code is 0
