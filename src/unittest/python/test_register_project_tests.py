"""class for testing the regsiter_order method"""
import unittest
from datetime import date

from uc3m_consulting import EnterpriseManager
from uc3m_consulting import EnterpriseManagerException

class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""
    def test_valid_1( self ):
        importe = 50000.00
        my_manager = EnterpriseManager()
        valor_devuelto = my_manager.register_project(company_cif=cif, project_acronym=acronym,
                                                     project_description=description, date=date,
                                                     department=department, budget=importe)
        self.assertEqual(valor_devuelto, "84fb2cba79af99d1afee74619c")

    def test_register_2( self ):
        """Cif not valid"""
        my_manager = EnterpriseManager()
        cif = "A1234567"
        acronym = "PEPESL"
        description = "marketing de pepe"
        department = "FINANCE"
        date = "01/01/2025"
        budget = 100000.00
        with self.assertRaises(EnterpriseManagerException) as cm:
            result = my_manager.register_project(company_cif=cif, project_acronym=acronym,
                                                 project_description=description, date=date,
                                                 department=department, budget=budget)
        self.assertEqual(cm.exception.message, "ERROR: CIF not valid, length")


if __name__ == '__main__':
    unittest.main()