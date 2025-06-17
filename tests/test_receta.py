import unittest
from src.receta import Receta
from src.paciente import Paciente
from src.medico import Medico
from src.especialidad import Especialidad


class TestReceta(unittest.TestCase):
    def setUp(self):
        self.paciente = Paciente("Juan Pérez", "12345678", "12/12/1990")
        self.medico = Medico("Dr. Carlos Gómez", "1234")
        self.medico.agregar_especialidad(Especialidad("Pediatría", ["lunes"]))
        
        self.medicamentos = ["Paracetamol", "Ibuprofeno"]
        self.receta = Receta(self.paciente, self.medico, self.medicamentos)

    def test_obtener_paciente(self):
        self.assertEqual(self.receta.obtener_paciente(), self.paciente)

    def test_obtener_medico(self):
        self.assertEqual(self.receta.obtener_medico(), self.medico)

    def test_obtener_medicamentos(self):
        medicamentos = self.receta.obtener_medicamentos()
        self.assertEqual(medicamentos, ["Paracetamol", "Ibuprofeno"])

    def test_obtener_fecha(self):
        fecha = self.receta.obtener_fecha()
        self.assertIsNotNone(fecha)

    def test_str(self):
        receta_str = str(self.receta)
        self.assertIn("Juan Pérez", receta_str)
        self.assertIn("Dr. Carlos Gómez", receta_str)
        self.assertIn("Paracetamol", receta_str)
        self.assertIn("Ibuprofeno", receta_str)


if _name_ == "_main_":
    unittest.main()