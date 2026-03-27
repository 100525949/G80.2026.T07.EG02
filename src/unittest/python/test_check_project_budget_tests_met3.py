"""Tests para el Met. 3"""
import unittest
import os
import json
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

JSON_FILES_PATH = os.path.join(os.path.dirname(__file__), "../jsonfiles/")
FLOWS_FILE = os.path.join(JSON_FILES_PATH, "flows.json")
BALANCES_FILE = os.path.join(JSON_FILES_PATH, "project_balances.json")

class TestCheckProjectBudget(unittest.TestCase):
    """Clase de pruebas para el metodo 3"""

    def setUp(self):
        """Se ejecuta antes de cada test para preparar un entorno limpio"""
        os.makedirs(JSON_FILES_PATH, exist_ok=True)
        self._clean_files()
        self.manager = EnterpriseManager()
        self.valid_id = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"

    def tearDown(self):
        """Se ejecuta depues de cada test para no dejar rastro """
        self._clean_files()

    def _clean_files(self):
        """Borra los archivos si existen para evitar conflictos entre tests"""
        if os.path.exists(FLOWS_FILE):
            os.remove(FLOWS_FILE)
        if os.path.exists(BALANCES_FILE):
            os.remove(BALANCES_FILE)

    def _create_flows_file(self, content):
        """Crea el archivo flows.json con el contenido que le pasemos"""
        with open(FLOWS_FILE, "w", encoding="utf-8") as f:
            if isinstance(content, str):
                f.write(content)
            else:
                json.dump(content, f)

    def test_01_invalid_project_id(self):
        """Ruta 1: El ID no cumple el formato"""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.check_project_budget("ID_CORTO_O_INVALIDO")
        self.assertEqual(cm.exception.message, "ERROR: Invalid PROJECT_ID format")
