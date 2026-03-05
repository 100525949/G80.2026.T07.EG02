"""Module """

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

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
