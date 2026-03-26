"""class for testing the register_project method"""
import unittest
import os
from enterprise_manager import EnterpriseManager
from enterprise_management_exception import EnterpriseManagementException

class MyTestCase(unittest.TestCase):
    """class for testing the register_project method"""

    def setUp(self):
        """Se ejecuta antes de cada test para borrar el json y asegurar que los tests
        empiezan limpios"""
        json_path = os.path.join(os.path.dirname(__file__), "../../../unittest/corporate_operations.json")
        if os.path.exists(json_path):
            os.remove(json_path)

    def test_valid_1(self):
        """Caso válido base"""
        my_manager = EnterpriseManager()

        cif = "Q2812004I"
        acronym = "PROJ01"
        description = "Descripcion valida"
        department = "HR"
        date = "18/02/2026"
        budget = 50000.00

        valor_devuelto = my_manager.register_project(
            company_cif=cif,
            project_acronym=acronym,
            project_description=description,
            date=date,
            department=department,
            budget=budget
        )

        # comprobamos que devuelve un string de 32 caracteres
        self.assertIsInstance(valor_devuelto, str)
        self.assertEqual(len(valor_devuelto), 32)

    def test_register_2_cif_invalid(self):
        """Cif no valido (Longitud incorrecta)"""
        my_manager = EnterpriseManager()

        cif = "A1234567"  # CIF inválido
        acronym = "PROJ01"
        description = "Descripcion valida"
        department = "HR"
        date = "18/02/2026"
        budget = 100000.00

        with self.assertRaises(EnterpriseManagementException) as cm:
            my_manager.register_project(
                company_cif=cif,
                project_acronym=acronym,
                project_description=description,
                date=date,
                department=department,
                budget=budget
            )

        self.assertEqual(cm.exception.message, "ERROR: CIF format not valid")

if __name__ == '__main__':
    unittest.main()