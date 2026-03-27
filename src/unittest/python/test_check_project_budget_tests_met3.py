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

    def test_02_file_not_found(self):
        """Ruta 2.1: El archivo flows.json no existe"""
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.check_project_budget(self.valid_id)
        self.assertEqual(cm.exception.message, "ERROR: flows.json file not found")

    def test_03_invalid_json_format(self):
        """Ruta 2.2: El archivo existe pero está corrupto"""
        self._create_flows_file("{ este_json_esta_roto")
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.check_project_budget(self.valid_id)
        self.assertEqual(cm.exception.message, "ERROR: flows.json is not a valid JSON")

    def test_04_loop_0_times_project_not_found(self):
        """Ruta 3.1 (Bucle con 0 iteraciones o sin match): el json es una lista vacía"""
        self._create_flows_file([])
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.check_project_budget(self.valid_id)
        self.assertEqual(cm.exception.message, "ERROR: PROJECT_ID not found in flows.json")

    def test_05_loop_n_times_project_not_found(self):
        """Ruta 3.2: hay datos en el bucle, pero ninguno es nuestro proyecto, no nos valen"""
        data = [
            {"PROJECT_ID": "f6b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "inflow": "100"},
            {"PROJECT_ID": "c3d4e5f6a1b2c3d4e5f6a1b2c3d4a1b2", "outflow": "50"}
        ]
        self._create_flows_file(data)
        with self.assertRaises(EnterpriseManagementException) as cm:
            self.manager.check_project_budget(self.valid_id)
        self.assertEqual(cm.exception.message, "ERROR: PROJECT_ID not found in flows.json")

    def test_06_loop_1_time_success(self):
        """Ruta 4 (exito - bucle con 1 iteración): solo hay un solo registro y es nuestro proyecto"""
        data = [{"PROJECT_ID": self.valid_id, "inflow": "1500.50"}]
        self._create_flows_file(data)

        result = self.manager.check_project_budget(self.valid_id)
        self.assertTrue(result)

        # miramos si se guarda el balance bien
        with open(BALANCES_FILE, "r", encoding="utf-8") as f:
            balances = json.load(f)
            self.assertEqual(balances[0]["balance"], 1500.50)
            self.assertEqual(balances[0]["project_id"], self.valid_id)

    def test_07_loop_2_times_success(self):
        """Ruta 4 (exito - bucle con 2 iteraciones): un inflow + un outflow"""
        data = [
            {"PROJECT_ID": self.valid_id, "inflow": "2000.0"},
            {"PROJECT_ID": self.valid_id, "outflow": "500.0"}
        ]
        self._create_flows_file(data)

        result = self.manager.check_project_budget(self.valid_id)
        self.assertTrue(result)

        with open(BALANCES_FILE, "r", encoding="utf-8") as f:
            balances = json.load(f)
            self.assertEqual(balances[0]["balance"], 1500.0)  # 2000 - 500

    def test_08_loop_n_times_mixed_data_and_value_error(self):
        """Ruta 4 (exito - n iteraciones + Prueba de excepciones internas de valores raros)"""
        data = [
            {"PROJECT_ID": "otro_proyecto_ignorado", "inflow": "9999"},
            {"PROJECT_ID": self.valid_id, "inflow": "1000"},
            {"PROJECT_ID": self.valid_id, "outflow": "texto_invalido"},  # Entra al except ValueError
            {"PROJECT_ID": self.valid_id, "outflow": "300"}
        ]
        self._create_flows_file(data)

        result = self.manager.check_project_budget(self.valid_id)
        self.assertTrue(result)

        with open(BALANCES_FILE, "r", encoding="utf-8") as f:
            balances = json.load(f)
            self.assertEqual(balances[0]["balance"], 700.0)  # 1000 - 300 (el texto_invalido se ignora)

    def test_09_balances_file_corrupted(self):
        """Ruta 4b: recrea el archivo de balances si el anterior estaba corrupto"""
        self._create_flows_file([{"PROJECT_ID": self.valid_id, "inflow": "100"}])

        # corrompemos el archivo de salida
        with open(BALANCES_FILE, "w", encoding="utf-8") as f:
            f.write("esto no es un json")

        result = self.manager.check_project_budget(self.valid_id)
        self.assertTrue(result)

        with open(BALANCES_FILE, "r", encoding="utf-8") as f:
            balances = json.load(f)
            self.assertEqual(balances[0]["balance"], 100.0)

if __name__ == '__main__':
    unittest.main()