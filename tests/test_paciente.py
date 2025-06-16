import unittest
from src.paciente import Paciente

class TestPaciente(unittest.TestCase):
    def setUp(self):
        self.paciente = Paciente("Juan Pérez", "12345678", "1985-01-01")

    def test_str(self):
        self.assertIn("Juan Pérez", str(self.paciente))
        self.assertIn("12345678", str(self.paciente))

    def test_obtener_dni(self):
        self.assertEqual(self.paciente.obtener_dni(), "12345678")

if __name__ == '__main__':
    unittest.main()
