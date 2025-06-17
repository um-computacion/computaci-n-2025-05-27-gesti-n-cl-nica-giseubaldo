import unittest
from datetime import datetime
from src.turno import Turno
from src.paciente import Paciente
from src.medico import Medico
from src.especialidad import Especialidad


class TestTurno(unittest.TestCase):
    def setUp(self):
        self.paciente = Paciente("Juan Pérez", "12345678", "12/12/1990")
        self.medico = Medico("Dr. Carlos Gómez", "1234")
        self.medico.agregar_especialidad(Especialidad("Pediatría", ["lunes"]))
        
        self.fecha_hora = datetime(2026, 6, 1, 10, 0)
        self.especialidad = "Pediatría"
        self.turno = Turno(self.paciente, self.medico, self.fecha_hora, self.especialidad)

    def test_obtener_medico(self):
        self.assertEqual(self.turno.obtener_medico(), self.medico)

    def test_obtener_paciente(self):
        self.assertEqual(self.turno.obtener_paciente(), self.paciente)

    def test_obtener_fecha_hora(self):
        self.assertEqual(self.turno.obtener_fecha_hora(), self.fecha_hora)

    def test_obtener_especialidad(self):
        self.assertEqual(self.turno.obtener_especialidad(), self.especialidad)

    def test_str(self):
        turno_str = str(self.turno)
        self.assertIn("Juan Pérez", turno_str)
        self.assertIn("Dr. Carlos Gómez", turno_str)
        self.assertIn("Pediatría", turno_str)
        self.assertIn("01/06/2026", turno_str)


if _name_ == "_main_":
    unittest.main()