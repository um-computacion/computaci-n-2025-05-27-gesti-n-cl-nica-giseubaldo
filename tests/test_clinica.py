import unittest
from datetime import datetime, timedelta
from src.clinica import Clinica
from src.paciente import Paciente
from src.medico import Medico
from src.especialidad import Especialidad
from src.excepciones import (
    PacienteNoEncontradoException,
    MedicoNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    RecetaInvalidaException,
    PacienteDuplicadoException,
    MedicoDuplicadoException,
    DatosInvalidosException
)


class TestClinica(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.clinica = Clinica()
        
        # Pacientes de prueba
        self.paciente1 = Paciente("Juan Pérez", "12345678", "12/12/1990")
        self.paciente2 = Paciente("Ana López", "87654321", "01/01/1985")
        
        # Médicos de prueba
        self.medico1 = Medico("Dr. Carlos Gómez", "1234")
        self.medico1.agregar_especialidad(Especialidad("Pediatría", ["lunes", "miércoles", "viernes"]))
        
        self.medico2 = Medico("Dra. María García", "5678")
        self.medico2.agregar_especialidad(Especialidad("Cardiología", ["martes", "jueves"]))

    # PRUEBAS DE PACIENTES Y MÉDICOS
    
    def test_registro_exitoso_paciente(self):
        """Prueba registro exitoso de pacientes."""
        self.clinica.agregar_paciente(self.paciente1)
        pacientes = self.clinica.obtener_pacientes()
        self.assertEqual(len(pacientes), 1)
        self.assertEqual(pacientes[0].obtener_dni(), "12345678")

    def test_registro_exitoso_medico(self):
        """Prueba registro exitoso de médicos."""
        self.clinica.agregar_medico(self.medico1)
        medicos = self.clinica.obtener_medicos()
        self.assertEqual(len(medicos), 1)
        self.assertEqual(medicos[0].obtener_matricula(), "1234")

    def test_prevencion_paciente_duplicado(self):
        """Prueba prevención de registros duplicados por DNI."""
        self.clinica.agregar_paciente(self.paciente1)
        paciente_duplicado = Paciente("Juan Martínez", "12345678", "15/03/1992")
        
        with self.assertRaises(PacienteDuplicadoException):
            self.clinica.agregar_paciente(paciente_duplicado)

    def test_prevencion_medico_duplicado(self):
        """Prueba prevención de registros duplicados por matrícula."""
        self.clinica.agregar_medico(self.medico1)
        medico_duplicado = Medico("Dr. Pedro Rodríguez", "1234")
        
        with self.assertRaises(MedicoDuplicadoException):
            self.clinica.agregar_medico(medico_duplicado)

    def test_datos_invalidos_paciente(self):
        """Prueba verificación de errores por datos inválidos en paciente."""
        with self.assertRaises(DatosInvalidosException):
            self.clinica.agregar_paciente("no es un paciente")

    def test_datos_invalidos_medico(self):
        """Prueba verificación de errores por datos inválidos en médico."""
        with self.assertRaises(DatosInvalidosException):
            self.clinica.agregar_medico("no es un médico")

    # PRUEBAS DE ESPECIALIDADES

    def test_agregar_especialidad_medico_registrado(self):
        """Prueba agregar especialidades nuevas a un médico ya registrado."""
        self.clinica.agregar_medico(self.medico1)
        medico = self.clinica.obtener_medico_por_matricula("1234")
        
        nueva_especialidad = Especialidad("Neurología", ["sábado"])
        medico.agregar_especialidad(nueva_especialidad)
        
        especialidades = medico.obtener_especialidades()
        self.assertEqual(len(especialidades), 2)

    def test_error_medico_no_registrado(self):
        """Prueba error si se intenta obtener un médico no registrado."""
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.obtener_medico_por_matricula("9999")

    # PRUEBAS DE TURNOS

    def test_agendar_turno_exitoso(self):
        """Prueba agendamiento exitoso de turnos."""
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        # Usar fecha futura fija que es lunes
        fecha_turno = datetime(2026, 6, 1, 10, 0)  # 1 de junio de 2026 es lunes
        
        self.clinica.agendar_turno("12345678", "1234", "Pediatría", fecha_turno)
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)

    def test_evitar_turnos_duplicados(self):
        """Prueba evitar turnos duplicados (mismo médico y fecha/hora)."""
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_paciente(self.paciente2)
        self.clinica.agregar_medico(self.medico1)
        
        fecha_turno = datetime(2026, 6, 1, 10, 0)  # 1 de junio de 2026 es lunes
        
        # Primer turno
        self.clinica.agendar_turno("12345678", "1234", "Pediatría", fecha_turno)
        
        # Intento de turno duplicado
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("87654321", "1234", "Pediatría", fecha_turno)

    def test_error_paciente_no_existe_turno(self):
        """Prueba error si el paciente no existe al agendar turno."""
        self.clinica.agregar_medico(self.medico1)
        fecha_turno = datetime(2026, 6, 1, 10, 0)  # 1 de junio de 2026 es lunes
        
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno("99999999", "1234", "Pediatría", fecha_turno)

    def test_error_medico_no_existe_turno(self):
        """Prueba error si el médico no existe al agendar turno."""
        self.clinica.agregar_paciente(self.paciente1)
        fecha_turno = datetime(2026, 6, 1, 10, 0)  # 1 de junio de 2026 es lunes
        
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.agendar_turno("12345678", "9999", "Pediatría", fecha_turno)

    def test_error_especialidad_no_disponible(self):
        """Prueba error si el médico no atiende la especialidad solicitada."""
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        fecha_turno = datetime(2026, 6, 1, 10, 0)  # 1 de junio de 2026 es lunes
        
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "1234", "Cardiología", fecha_turno)

    def test_error_medico_no_trabaja_ese_dia(self):
        """Prueba error si el médico no trabaja ese día de la semana."""
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        # Martes (médico no trabaja martes) - 2 de junio de 2026 es martes
        fecha_turno = datetime(2026, 6, 2, 10, 0)
        
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "1234", "Pediatría", fecha_turno)

    # PRUEBAS DE RECETAS

    def test_emitir_receta_exitosa(self):
        """Prueba emisión exitosa de recetas."""
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        self.clinica.emitir_receta("12345678", "1234", ["Paracetamol", "Ibuprofeno"])
        
        historia = self.clinica.obtener_historia_clinica("12345678")
        recetas = historia.obtener_recetas()
        self.assertEqual(len(recetas), 1)

    def test_error_paciente_no_existe_receta(self):
        """Prueba error si el paciente no existe al emitir receta."""
        self.clinica.agregar_medico(self.medico1)
        
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.emitir_receta("99999999", "1234", ["Paracetamol"])

    def test_error_medico_no_existe_receta(self):
        """Prueba error si el médico no existe al emitir receta."""
        self.clinica.agregar_paciente(self.paciente1)
        
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.emitir_receta("12345678", "9999", ["Paracetamol"])

    def test_error_medicamentos_vacios(self):
        """Prueba error si no hay medicamentos listados."""
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("12345678", "1234", [])

    # PRUEBAS DE HISTORIA CLÍNICA

    def test_obtener_historia_clinica_completa(self):
        """Prueba obtener la historia clínica completa de un paciente."""
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        # Agendar turno
        fecha_turno = datetime(2026, 6, 1, 10, 0)  # 1 de junio de 2026 es lunes
        self.clinica.agendar_turno("12345678", "1234", "Pediatría", fecha_turno)
        
        # Emitir receta
        self.clinica.emitir_receta("12345678", "1234", ["Paracetamol"])
        
        historia = self.clinica.obtener_historia_clinica("12345678")
        turnos = historia.obtener_turnos()
        recetas = historia.obtener_recetas()
        
        self.assertEqual(len(turnos), 1)
        self.assertEqual(len(recetas), 1)

    def test_error_historia_paciente_no_registrado(self):
        """Prueba error al obtener historia clínica de paciente no registrado."""
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.obtener_historia_clinica("99999999")

    # MÉTODOS AUXILIARES

    def _obtener_proximo_lunes(self):
        """Obtiene la fecha del próximo lunes."""
        hoy = datetime.now()
        dias_hasta_lunes = (0 - hoy.weekday()) % 7  # 0 = lunes
        if dias_hasta_lunes == 0:  # Si hoy es lunes, tomar el siguiente
            dias_hasta_lunes = 7
        return hoy + timedelta(days=dias_hasta_lunes)

    def _obtener_proximo_martes(self):
        """Obtiene la fecha del próximo martes."""
        hoy = datetime.now()
        dias_hasta_martes = (1 - hoy.weekday()) % 7  # 1 = martes
        if dias_hasta_martes == 0:  # Si hoy es martes, tomar el siguiente
            dias_hasta_martes = 7
        return hoy + timedelta(days=dias_hasta_martes)

    def _obtener_fecha_fija_lunes(self):
        """Obtiene una fecha fija que es lunes para pruebas consistentes."""
        # 4 de noviembre de 2024 es lunes
        return datetime(2024, 11, 4, 10, 0)

    def _obtener_fecha_fija_martes(self):
        """Obtiene una fecha fija que es martes para pruebas consistentes."""
        # 5 de noviembre de 2024 es martes
        return datetime(2024, 11, 5, 10, 0)


if __name__ == "_main_":
    unittest.main()