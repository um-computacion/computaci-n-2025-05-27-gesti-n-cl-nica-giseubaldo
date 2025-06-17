import unittest
from src.paciente import Paciente
from src.excepciones import DatosInvalidosException


class TestPaciente(unittest.TestCase):
    
    def test_creacion_paciente_exitosa(self):
        """Prueba la creación exitosa de un paciente."""
        paciente = Paciente("Juan Pérez", "12345678", "12/12/2000")
        self.assertEqual(paciente.obtener_dni(), "12345678")
        self.assertEqual(paciente.obtener_nombre(), "Juan Pérez")
        self.assertEqual(paciente.obtener_fecha_nacimiento(), "12/12/2000")
        self.assertEqual(str(paciente), "Juan Pérez, 12345678, 12/12/2000")

    def test_nombre_vacio(self):
        """Prueba error cuando el nombre está vacío."""
        with self.assertRaises(DatosInvalidosException):
            Paciente("", "12345678", "12/12/2000")

    def test_nombre_solo_espacios(self):
        """Prueba error cuando el nombre son solo espacios."""
        with self.assertRaises(DatosInvalidosException):
            Paciente("   ", "12345678", "12/12/2000")

    def test_nombre_con_caracteres_invalidos(self):
        """Prueba error cuando el nombre contiene caracteres inválidos."""
        with self.assertRaises(DatosInvalidosException):
            Paciente("Juan123", "12345678", "12/12/2000")

    def test_dni_vacio(self):
        """Prueba error cuando el DNI está vacío."""
        with self.assertRaises(DatosInvalidosException):
            Paciente("Juan Pérez", "", "12/12/2000")

    def test_dni_muy_corto(self):
        """Prueba error cuando el DNI es muy corto."""
        with self.assertRaises(DatosInvalidosException):
            Paciente("Juan Pérez", "123456", "12/12/2000")

    def test_dni_muy_largo(self):
        """Prueba error cuando el DNI es muy largo."""
        with self.assertRaises(DatosInvalidosException):
            Paciente("Juan Pérez", "123456789", "12/12/2000")

    def test_dni_con_letras(self):
        """Prueba error cuando el DNI contiene letras."""
        with self.assertRaises(DatosInvalidosException):
            Paciente("Juan Pérez", "1234567A", "12/12/2000")

    def test_fecha_vacia(self):
        """Prueba error cuando la fecha está vacía."""
        with self.assertRaises(DatosInvalidosException):
            Paciente("Juan Pérez", "12345678", "")

    def test_fecha_formato_incorrecto(self):
        """Prueba error cuando la fecha tiene formato incorrecto."""
        with self.assertRaises(DatosInvalidosException):
            Paciente("Juan Pérez", "12345678", "2000-12-12")

    def test_fecha_invalida(self):
        """Prueba error cuando la fecha es inválida."""
        with self.assertRaises(DatosInvalidosException):
            Paciente("Juan Pérez", "12345678", "32/13/2000")

    def test_dni_diferente(self):
        """Prueba que pacientes diferentes tienen DNIs diferentes."""
        paciente1 = Paciente("Juan Pérez", "12345678", "12/12/2000")
        paciente2 = Paciente("Ana López", "87654321", "01/01/1990")
        self.assertNotEqual(paciente1.obtener_dni(), paciente2.obtener_dni())


if __name__ == "__main__":
    unittest.main()