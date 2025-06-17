from datetime import datetime
from .paciente import Paciente
from .medico import Medico
from .turno import Turno
from .receta import Receta
from .historiaclinica import HistoriaClinica
from .excepciones import (
    PacienteNoEncontradoException,
    MedicoNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    PacienteDuplicadoException,
    MedicoDuplicadoException,
    DatosInvalidosException
)

class Clinica:
    def __init__(self):
        self.__pacientes = {}  
        self.__medicos = {}    
        self.__turnos = []
        self.__historias_clinicas = {} 

    def agregar_paciente(self, paciente: Paciente):
        """Registra un paciente y crea su historia clínica."""
        if not isinstance(paciente, Paciente):
            raise DatosInvalidosException("El parámetro debe ser una instancia de Paciente")
        
        dni = paciente.obtener_dni()
        if dni in self.__pacientes:
            raise PacienteDuplicadoException(f"Ya existe un paciente con DNI {dni}")
        
        self.__pacientes[dni] = paciente
        self.__historias_clinicas[dni] = HistoriaClinica(paciente)

    def agregar_medico(self, medico: Medico):
        """Registra un médico."""
        if not isinstance(medico, Medico):
            raise DatosInvalidosException("El parámetro debe ser una instancia de Medico")
        
        matricula = medico.obtener_matricula()
        if matricula in self.__medicos:
            raise MedicoDuplicadoException(f"Ya existe un médico con matrícula {matricula}")
        
        self.__medicos[matricula] = medico

    def obtener_pacientes(self) -> list[Paciente]:
        """Devuelve todos los pacientes registrados."""
        return list(self.__pacientes.values())

    def obtener_medicos(self) -> list[Medico]:
        """Devuelve todos los médicos registrados."""
        return list(self.__medicos.values())

    def obtener_medico_por_matricula(self, matricula: str) -> Medico:
        """Devuelve un médico por su matrícula."""
        self.validar_existencia_medico(matricula)
        return self.__medicos[matricula]

    def agendar_turno(self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime):
        """Agenda un turno si se cumplen todas las condiciones."""
        # Validar que existan paciente y médico
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        
        paciente = self.__pacientes[dni]
        medico = self.__medicos[matricula]
        
        # Validar que no haya turno duplicado
        self.validar_turno_no_duplicado(matricula, fecha_hora)
        
        # Obtener día de la semana en español
        dia_semana = self.obtener_dia_semana_en_espanol(fecha_hora)
        
        # Validar que el médico atienda esa especialidad ese día
        self.validar_especialidad_en_dia(medico, especialidad, dia_semana)
        
        # Crear y agendar el turno
        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos.append(turno)
        
        # Agregar a la historia clínica
        self.__historias_clinicas[dni].agregar_turno(turno)

    def obtener_turnos(self) -> list[Turno]:
        """Devuelve todos los turnos agendados."""
        return self.__turnos.copy()

    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str]):
        """Emite una receta para un paciente."""
        # Validar que existan paciente y médico
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        
        paciente = self.__pacientes[dni]
        medico = self.__medicos[matricula]
        
        # Crear y emitir la receta
        receta = Receta(paciente, medico, medicamentos)
        
        # Agregar a la historia clínica
        self.__historias_clinicas[dni].agregar_receta(receta)

    def obtener_historia_clinica(self, dni: str) -> HistoriaClinica:
        """Devuelve la historia clínica completa de un paciente."""
        self.validar_existencia_paciente(dni)
        return self.__historias_clinicas[dni]

    def validar_existencia_paciente(self, dni: str):
        """Verifica si un paciente está registrado."""
        if not dni or dni not in self.__pacientes:
            raise PacienteNoEncontradoException(f"No se encontró un paciente con DNI {dni}")

    def validar_existencia_medico(self, matricula: str):
        """Verifica si un médico está registrado."""
        if not matricula or matricula not in self.__medicos:
            raise MedicoNoEncontradoException(f"No se encontró un médico con matrícula {matricula}")

    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime):
        """Verifica que no haya un turno duplicado."""
        for turno in self.__turnos:
            if (turno.obtener_medico().obtener_matricula() == matricula and 
                turno.obtener_fecha_hora() == fecha_hora):
                raise TurnoOcupadoException(f"El médico ya tiene un turno agendado para {fecha_hora.strftime('%d/%m/%Y %H:%M')}")

    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        """Traduce un objeto datetime al día de la semana en español."""
        dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        return dias_semana[fecha_hora.weekday()]

    def obtener_especialidad_disponible(self, medico: Medico, dia_semana: str) -> str:
        """Obtiene la especialidad disponible para un médico en un día."""
        especialidad = medico.obtener_especialidad_para_dia(dia_semana)
        if not especialidad:
            raise MedicoNoDisponibleException(f"El médico no atiende los {dia_semana}")
        return especialidad

    def validar_especialidad_en_dia(self, medico: Medico, especialidad_solicitada: str, dia_semana: str):
        """Verifica que el médico atienda esa especialidad ese día."""
        especialidad_disponible = medico.obtener_especialidad_para_dia(dia_semana)
        
        if not especialidad_disponible:
            raise MedicoNoDisponibleException(f"El Dr. {medico.obtener_nombre()} no atiende los {dia_semana}")
        
        if especialidad_disponible.lower() != especialidad_solicitada.lower():
            raise MedicoNoDisponibleException(
                f"El Dr. {medico.obtener_nombre()} no atiende {especialidad_solicitada} los {dia_semana}. "
                f"Ese día atiende: {especialidad_disponible}"
            )