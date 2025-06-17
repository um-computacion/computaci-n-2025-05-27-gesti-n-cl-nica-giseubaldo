import unittest
from src.especialidad import Especialidad


class TestEspecialidad(unittest.TestCase):

    def setUp(self):
        self.especialidad = Especialidad("Pediatría", ["lunes", "Miércoles", "VIERNES"])

    def test_obtener_especialidad(self):
        self.assertEqual(self.especialidad.obtener_especialidad(), "Pediatría")

    def test_verificar_dia_valido_minuscula(self):
        self.assertTrue(self.especialidad.verificar_dia("lunes"))

    def test_verificar_dia_valido_mayuscula(self):
        self.assertTrue(self.especialidad.verificar_dia("MIÉRCOLES"))

    def test_verificar_dia_valido_mixto(self):
        self.assertTrue(self.especialidad.verificar_dia("Viernes"))

    def test_verificar_dia_invalido(self):
        self.assertFalse(self.especialidad.verificar_dia("domingo"))

    def test_str(self):
        representacion = str(self.especialidad)
        self.assertIn("Pediatría", representacion)
        self.assertIn("lunes", representacion)
        self.assertIn("miércoles", representacion)
        self.assertIn("viernes", representacion)


if __name__ == "__main__":
    unittest.main()
