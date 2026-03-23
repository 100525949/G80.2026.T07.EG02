"""Module """
import re
import os
import json

from enterprise_management_exception import EnterpriseManagementException
from enterprise_project import EnterpriseProject
class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def register_project(self, company_cif: str, project_acronym: str,
                         project_description: str, date: str,
                         department: str, budget: float) -> str:
        self.validate_cif(company_cif)
        my_project = EnterpriseProject(company_cif=company_cif, project_acronym=project_acronym,
                                       department=department, project_budget=budget,
                                       project_description=project_description, starting_date=date)


        JSON_FILES_PATH = os.path.join( os.path.dirname(__file__), "../../../unittest/")
        file_store = JSON_FILES_PATH + "register_store.json"
        try:
            with open(file_store, "r", encoding="utf-8",newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError as ex:
            data_list = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSOn Format")

        data_list.append(my_project.to_json())




    @staticmethod
    def validate_cif(cif: str):
        cif = cif.upper()

        if not re.match(r'^[ABEHKPQS][0-9]{7}[0-9A-J]$', cif):
            raise EnterpriseManagementException("ERROR: CIF format not valid")

        letras_tipo = cif[0]
        digitos = cif[1:8]
        control = cif[8]

        suma_pares = sum(int(digitos[i]) for i in range(1, len(digitos), 2))

        suma_impares = 0
        for i in range(0, len(digitos), 2):
            res = int(digitos[i]) * 2
            suma_impares += (res // 10) + (res % 10)

        suma_total = suma_impares + suma_pares
        unidad = suma_total % 10

        num_control = (10 - unidad) % 10
        letra_control = 'JABCDEFGHI'[num_control]

        if letras_tipo in 'ABEH':
            return control == str(num_control)
        elif letras_tipo in 'KPQS':
            return control == letra_control
        else:
            return False

        pass
