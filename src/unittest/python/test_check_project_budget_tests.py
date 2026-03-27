"""Tests para el Met. 3"""
import unittest
import os
import json
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

JSON_FILES_PATH = os.path.join(os.path.dirname(__file__), "../jsonfiles/")
FLOWS_FILE = os.path.join(JSON_FILES_PATH, "flows.json")
BALANCES_FILE = os.path.join(JSON_FILES_PATH, "project_balances.json")


