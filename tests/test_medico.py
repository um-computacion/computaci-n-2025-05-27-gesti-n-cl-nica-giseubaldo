import unittest

from src.medico import Medico
from src.especialidad import Especialidad


class TestMedico(unittest.TestCase):

    def setUp(self):
        self.medico = Medico("Carlos López", "M1234")
        self.pediatria = Especialidad("Pediatría", ["lunes", "miércoles"])
        self.cardiologia = Especialidad("Cardiología", ["martes"])

    def test_obtener_matricula(self):
        self.assertEqual(self.medico.obtener_matricula(), "M1234")

    def test_agregar_especialidad(self):
        self.medico.agregar_especialidad(self.pediatria)
        self.assertEqual(self.medico._especialidades[0].obtener_especialidad(), "Pediatría")

    def test_especialidad_para_dia_existente(self):
        self.medico.agregar_especialidad(self.pediatria)
        self.assertEqual(self.medico.obtener_especialidad_para_dia("LUNES"), "Pediatría")

    def test_especialidad_para_dia_inexistente(self):
        self.medico.agregar_especialidad(self.pediatria)
        self.assertIsNone(self.medico.obtener_especialidad_para_dia("viernes"))

    def test_multiple_especialidades(self):
        self.medico.agregar_especialidad(self.pediatria)
        self.medico.agregar_especialidad(self.cardiologia)
        self.assertEqual(self.medico.obtener_especialidad_para_dia("martes"), "Cardiología")


if __name__ == "__main__":
    unittest.main()

