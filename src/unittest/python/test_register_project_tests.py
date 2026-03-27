"""class for testing the register_project method"""
import unittest
import os
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

JSON_FILES_PATH = os.path.join( os.path.dirname(__file__), "../jsonfiles/")
file_store = JSON_FILES_PATH + "corporate_operations.json"

class MyTestCase(unittest.TestCase):
    """class for testing the register_project method"""

    # tests metodo 1

    def setUp(self):
        """Se ejecuta antes de cada test para borrar el json y asegurar que los tests
        empiezan limpios"""
        json_path = os.path.join(os.path.dirname(__file__), "../corporate_operations.json")
        if os.path.exists(json_path):
            os.remove(json_path)

    def test_01_valid(self):
        """Test 1 valido -> Caso válido base"""
        my_manager = EnterpriseManager()
        valor_devuelto = my_manager.register_project(
            company_cif="Q2812004F", project_acronym="PROJ01",
            project_description="Descrip valida", department="HR",
            date="18/02/2026", budget=100000.00
        )
        self.assertIsInstance(valor_devuelto, str)
        self.assertEqual(len(valor_devuelto), 32)

    def test_02_valid(self):
        """Test 2 valido -> acrónimo límite inferior (5 char)"""
        my_manager = EnterpriseManager()
        valor_devuelto = my_manager.register_project(
            company_cif="Q2812004F", project_acronym="PROJ0",
            project_description="Descrip valida", department="HR",
            date="18/02/2026", budget=100000.00
        )
        self.assertEqual(len(valor_devuelto), 32)

    def test_03_valid(self):
        """Test 3 valido -> Acrónimo límite superior (10 char)"""
        my_manager = EnterpriseManager()
        valor_devuelto = my_manager.register_project(
            company_cif="Q2812004F", project_acronym="PROJ012345",
            project_description="Descrip valida", department="HR",
            date="18/02/2026", budget=100000.00
        )
        self.assertEqual(len(valor_devuelto), 32)

    def test_04_valid(self):
        """Test 4 valido -> Presupuesto límite inferior (50k)"""
        my_manager = EnterpriseManager()
        valor_devuelto = my_manager.register_project(
            company_cif="Q2812004F", project_acronym="PROJ01",
            project_description="Descrip valida", department="HR",
            date="18/02/2026", budget=50000.00
        )
        self.assertEqual(len(valor_devuelto), 32)

    def test_05_invalid(self):
        """Test 5 invalido -> Acrónimo límite inferior (4 char)"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project("Q2812004F", "PROJ", "Descrip valida", "18/02/2026", "HR", 100000.00)
        self.assertEqual(cm.exception.message, "ERROR: Acronym length not valid")

    def test_06_invalid(self):
        """Test 6 invalido -> Acrónimo límite superior (11 char)"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project("Q2812004F", "PROJ0123456", "Descrip valida", "18/02/2026", "HR", 100000.00)
        self.assertEqual(cm.exception.message, "ERROR: Acronym length not valid")

    def test_07_invalid(self):
        """Test 7 invalido -> Acrónimo caracteres no válidos"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project("Q2812004F", "PR-J01", "Descrip valida", "18/02/2026", "HR", 100000.00)
        self.assertEqual(cm.exception.message, "ERROR: Acronym format not valid")

    def test_08_invalid(self):
        """Test 8 -> Descripción límite inf. (9 char)"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project("Q2812004F", "PROJ01", "Descr. 9c", "18/02/2026", "HR", 100000.00)
        self.assertEqual(cm.exception.message, "ERROR: Description length not valid")

    def test_09_invalid(self):
        """Test 9 -> Descripción límite sup. (31 char)"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project("Q2812004F", "PROJ01", "Esta descripcion tiene 31 chars", "18/02/2026", "HR",
                                        100000.00)
        self.assertEqual(cm.exception.message, "ERROR: Description length not valid")

    def test_10_invalid(self):
        """Test 10 -> Departamento no permitido"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project("Q2812004F", "PROJ01", "Descrip valida", "18/02/2026", "IT", 100000.00)
        self.assertEqual(cm.exception.message, "ERROR: Department not valid")

    def test_11_invalid(self):
        """Test 11 -> Fecha anterior a 2025"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project("Q2812004F", "PROJ01", "Descrip valida", "31/12/2024", "HR", 100000.00)
        self.assertEqual(cm.exception.message, "ERROR: Date out of range")

    def test_12_invalid(self):
        """Test 12 -> Fecha posterior a 2027"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project("Q2812004F", "PROJ01", "Descrip valida", "01/01/2028", "HR", 100000.00)
        self.assertEqual(cm.exception.message, "ERROR: Date out of range")

    def test_13_invalid(self):
        """Test 13 -> Fecha formato incorrecto"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project("Q2812004F", "PROJ01", "Descrip valida", "18-02-2026", "HR", 100000.00)
        self.assertEqual(cm.exception.message, "ERROR: Date format not valid")

    def test_14_invalid(self):
        """Test 14 -> Presupuesto límite inf. (< 50k)"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project("Q2812004F", "PROJ01", "Descrip valida", "18/02/2026", "HR", 49999.99)
        self.assertEqual(cm.exception.message, "ERROR: Budget out of range")

    def test_15_invalid(self):
        """Test 15 -> Presupuesto límite sup. (> 1M)"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project("Q2812004F", "PROJ01", "Descrip valida", "18/02/2026", "HR", 1000000.01)
        self.assertEqual(cm.exception.message, "ERROR: Budget out of range")

    def test_16_invalid(self):
        """Test 16 -> CIF longitud incorrecta"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project("Q2812004", "PROJ01", "Descrip valida", "18/02/2026", "HR", 100000.00)
        self.assertEqual(cm.exception.message, "ERROR: CIF format not valid")

    def test_17_invalid(self):
        """Test 17 -> CIF letra control incorrecta"""
        my_manager = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project("Q2812004A", "PROJ01", "Descrip valida", "18/02/2026", "HR", 100000.00)
        self.assertEqual(cm.exception.message, "ERROR: CIF not valid")

    # tests del metodo 2
    def _create_temp_file(self, filename: str, content: str) -> str:
        """función para crear archivos json temporales en los tests"""
        file_path = os.path.join(JSON_FILES_PATH, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    def test_18_valid(self):
        """Test 1 metodo 2 -> Caso válido base"""
        content = '{"PROJECT_ID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "FILENAME": "docum001.pdf"}'
        file_path = self._create_temp_file("test_01_valid.json", content)

        my_manager = EnterpriseManager()
        valor_devuelto = my_manager.register_document(file_path)

        self.assertIsInstance(valor_devuelto, str)
        self.assertEqual(len(valor_devuelto), 64)
        os.remove(file_path)

if __name__ == '__main__':
    unittest.main()