"""Module """
import re
import os
import json
from project_document import ProjectDocument

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

        with open (file_store, "w", encoding="utf-8", newline="") as file:
            json.dump(data_list, file, indent=2)

        return my_project.project_id



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

    def register_document(self, input_file: str ) -> str:

        try:
            with open(input_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise EnterpriseManagementException("Error : Input file not found")
        except json.JSONDecodeError:
            raise EnterpriseManagementException("Error: File is not valid JSON")


        if "PROJECT_ID" not in data or "FILENAME" not in data:
            raise EnterpriseManagementException("Error: JSON missing required keys")

        project_id = data["PROJECT_ID"]
        filename = data["FILENAME"]

        if not re.match(r'^[0-9a-f]{32}$',project_id):
            raise EnterpriseManagementException("Error:PROJECT_ID not valid")
        if not re.match(r'^[a-zA-Z0-9]{8}\.(pdf|docx|xlsx)$',filename):
            raise EnterpriseManagementException("Error: FILENAME not valid")

        try:
            doc = ProjectDocument(project_id=project_id, file_name=filename)
            signature = doc.document_signature
        except Exception as ex :
            raise EnterpriseManagementException("Error: Internal processing error") from ex

        JSON_FILES_PATH = os.path.join(os.path.dirname(__file__),"../../../unittest/")
        file_store = JSON_FILES_PATH + "document_store.json"
        try:
            with open(file_store, "r", encoding="utf-8")as file:
                doc_list = json.load(file)
        except FileNotFoundError:
            doc_list = []
        except json.JSONDecodeError:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format")

        doc_list.append(doc.to_json())

        with open(file_store,"w", encoding="utf-8") as file:
            json.dump(doc_list, file, indent=2)

        return signature


