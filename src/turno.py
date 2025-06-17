from datetime import datetime
from .excepciones import DatosInvalidosException


class Turno:
    def _init_(self, paciente, medico, fecha_hora: datetime, especialidad: str):
        self._validar_parametros(paciente, medico, fecha_hora, especialidad)
        
        self.__paciente = paciente
        self.__medico = medico
        self.__fecha_hora = fecha_hora
        self.__especialidad = especialidad.strip()

    def _validar_parametros(self, paciente, medico, fecha_hora, especialidad):
        """Valida que todos los parámetros sean válidos."""
        if paciente is None:
            raise DatosInvalidosException("El paciente no puede ser None")
        
        if medico is None:
            raise DatosInvalidosException("El médico no puede ser None")
        
        if not isinstance(fecha_hora, datetime):
            raise DatosInvalidosException("La fecha_hora debe ser un objeto datetime")
        
        if fecha_hora < datetime.now():
            raise DatosInvalidosException("No se pueden agendar turnos en el pasado")
        
        if not especialidad or not especialidad.strip():
            raise DatosInvalidosException("La especialidad no puede estar vacía")

    def obtener_paciente(self):
        return self.__paciente

    def obtener_medico(self):
        return self.__medico

    def obtener_fecha_hora(self) -> datetime:
        return self.__fecha_hora

    def obtener_especialidad(self) -> str:
        return self.__especialidad

    def _str_(self) -> str:
        fecha_str = self.__fecha_hora.strftime("%d/%m/%Y %H:%M")
        return f"Turno: {self._paciente.obtener_nombre()}, Dr. {self.medico.obtener_nombre()}, {self._especialidad}, {fecha_str}"
