"""Module """
from src.main.python.uc3m_consulting import EnterpriseProject


class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def register_project(self, company_cif:str, project_acronym:str, project_description:str,
                         date:str, department:str, budget:float)->str:
        """Method for registering a new project"""
        my_project = EnterpriseProject(company_cif=company_cif, project_budget=budget,
                                       project_acronym=project_acronym, project_description=project_description,
                                       starting_date=date, department=department)
        return my_project.project_id

    @staticmethod
    def validate_cif(cif: str):
        # hay que poner aqui nuestra funcion validate_cif del ejercicio 1
        pass
