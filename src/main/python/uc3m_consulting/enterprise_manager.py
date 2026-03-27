"""Module """
import json
import re
import os
import hashlib
from datetime import datetime, timezone
from .enterprise_management_exception import EnterpriseManagementException
from .enterprise_project import EnterpriseProject

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    # metodo 1
    def register_project(self, company_cif: str, project_acronym: str,
                         project_description: str, date: str,
                         department: str, budget: float) -> str:
        self.validate_cif(company_cif)
        self.validate_acronym(project_acronym)
        self.validate_description(project_description)
        self.validate_department(department)
        self.validate_date(date)
        self.validate_budget(budget)

        my_project = EnterpriseProject(company_cif=company_cif, project_acronym=project_acronym,
                                       department=department, project_budget=budget,
                                       project_description=project_description, starting_date=date)


        JSON_FILES_PATH = os.path.join( os.path.dirname(__file__), "../../../unittest/")
        file_store = JSON_FILES_PATH + "corporate_operations.json"

        try:
            with open(file_store, "r", encoding="utf-8",newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            data_list = []
        except json.JSONDecodeError:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format")

        for item in data_list:
            if item.get("company_cif") == company_cif and item.get("project_acronym") == project_acronym:
                raise EnterpriseManagementException("ERROR: Project already exists")

        data_list.append(my_project.to_json())
        with open(file_store, "w", encoding="utf-8", newline="") as file:
            json.dump(data_list, file, indent=4)
        return my_project.project_id

    # metodo 2
    def register_document(self, input_file: str) -> str:
        """Registers a document from a JSON file and returns its SHA-256 signature"""
        # lee el json de entrada
        try:
            with open(input_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise EnterpriseManagementException("File is not found")
        except json.JSONDecodeError:
            raise EnterpriseManagementException("JSON Decode Error - File is not valid JSON")

        # se comprueba la estructura del json
        if not isinstance(data, dict) or "PROJECT_ID" not in data or "FILENAME" not in data:
            raise EnterpriseManagementException("JSON does not have the expected structure")

        project_id = data.get("PROJECT_ID")
        file_name = data.get("FILENAME")
        # se validan los valores
        if not isinstance(project_id, str) or not re.match(r'^[0-9a-fA-F]{32}$', project_id):
            raise EnterpriseManagementException("JSON data has invalid values: PROJECT_ID")

        if not isinstance(file_name, str) or not re.match(r'^[a-zA-Z0-9]{8}\.(pdf|docx|xlsx)$', file_name):
            raise EnterpriseManagementException("JSON data has invalid values: FILENAME")

        # calcular el sha
        alg = "SHA-256"
        typ = "DOCUMENT"
        justnow = datetime.now(timezone.utc)
        register_date = datetime.timestamp(justnow)

        text_to_encode = f"{{alg:{alg}, typ:{typ}, project_id:{project_id}, file_name:{file_name}}}"
        file_signature = hashlib.sha256(text_to_encode.encode()).hexdigest()

        document_data = {
            "alg": alg,
            "typ": typ,
            "project_id": project_id,
            "file_name": file_name,
            "register_date": register_date,
            "file_signature": file_signature
        }

        # guarda el documento firmado
        json_files_path = os.path.join(os.path.dirname(__file__), "../../../unittest/jsonfiles")
        store_file = os.path.join(json_files_path, "registered_documents.json")

        try:
            with open(store_file, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data_list = []

        data_list.append(document_data)

        try:
            with open(store_file, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=4)
        except Exception as e:
            raise EnterpriseManagementException("Internal error saving document") from e

        return file_signature

    # metodo 3
    def check_project_budget(self, project_id: str) -> bool:
        """Reads flows.json, calculates the budget for a project, and saves the result"""
        # valida que  project_id tiene formato hexadecimal
        if not isinstance(project_id, str) or not re.match(r'^[0-9a-fA-F]{32}$', project_id):
            raise EnterpriseManagementException("ERROR: Invalid PROJECT_ID format")

        # lee el flows.json
        json_files_path = os.path.join(os.path.dirname(__file__), "../../../unittest/jsonfiles/")
        flows_file = os.path.join(json_files_path, "flows.json")

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
        valid_control = False
        if letras_tipo in 'ABEH':
            valid_control = control == str(num_control)
        elif letras_tipo in 'KPQS':
            valid_control = control == letra_control

        if not valid_control:
            raise EnterpriseManagementException("ERROR: CIF not valid")

    @staticmethod
    def validate_acronym(acronym: str):
        """Valida longitud (5 a 10) y formato (solo alfanumérico)"""
        if not re.match(r'^[a-zA-Z0-9]+$', acronym):
            raise EnterpriseManagementException("ERROR: Acronym format not valid")
        if len(acronym) < 5 or len(acronym) > 10:
            raise EnterpriseManagementException("ERROR: Acronym length not valid")

    @staticmethod
    def validate_description(description: str):
        """Valida longitud de la descripción (10 a 30 caracteres)"""
        if len(description) < 10 or len(description) > 30:
            raise EnterpriseManagementException("ERROR: Description length not valid")

    @staticmethod
    def validate_department(department: str):
        """Valida que el departamento sea uno de los permitidos"""
        valid_departments = ["HR", "FINANCE", "LEGAL", "LOGISTICS"]
        if department not in valid_departments:
            raise EnterpriseManagementException("ERROR: Department not valid")

    @staticmethod
    def validate_date(date_str: str):
        """Valida el formato de fecha (DD/MM/YYYY) y el rango (2025 a 2027)"""
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            raise EnterpriseManagementException("ERROR: Date format not valid")

        if date_obj.year < 2025 or date_obj.year > 2027:
            raise EnterpriseManagementException("ERROR: Date out of range")

    @staticmethod
    def validate_budget(budget: float):
        """Valida que el presupuesto esté entre 50.000 y 1.000.000"""
        if budget < 50000.00 or budget > 1000000.00:
            raise EnterpriseManagementException("ERROR: Budget out of range")
