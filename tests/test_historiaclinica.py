import unittest
from src.historiaclinica import HistoriaClinica

class Dummy:
    def _init_(self, nombre):
        self.nombre = nombre
    def _str_(self):
        return self.nombre

class TestHistoriaClinica(unittest.TestCase):
    def setUp(self):
        self.paciente = Dummy("Paciente Test")
        self.turno = Dummy("Turno Test")
        self.receta = Dummy("Receta Test")
        self.historia = HistoriaClinica(self.paciente)

    def test_agregar_turno(self):
        self.historia.agregar_turno(self.turno)
        self.assertIn(self.turno, self.historia.obtener_turnos())

    def test_agregar_receta(self):
        self.historia.agregar_receta(self.receta)
        self.assertIn(self.receta, self.historia.obtener_recetas())

    def test_str(self):
        self.historia.agregar_turno(self.turno)
        self.historia.agregar_receta(self.receta)
        self.assertIn("Turno Test", str(self.historia))
        self.assertIn("Receta Test", str(self.historia))

if _name_ == "_main_":
    unittest.main()