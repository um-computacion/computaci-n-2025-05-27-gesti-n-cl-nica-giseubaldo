import unittest
from src.medico import Medico

class TestMedico(unittest.TestCase):
    def setUp(self):
        self.medico = Medico("Laura Pérez", "Dermatología", "D12345")

    def test_str(self):
        resultado = str(self.medico)
        self.assertIn("Laura Pérez", resultado)
        self.assertIn("Dermatología", resultado)
        self.assertIn("D12345", resultado)

    def test_obtener_matricula(self):
        self.assertEqual(self.medico.obtener_matricula(), "D12345")

if __name__ == "__main__":
    unittest.main()
