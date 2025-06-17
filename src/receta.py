from datetime import datetime
from .excepciones import DatosInvalidosException, RecetaInvalidaException


class Receta:
    def _init_(self, paciente, medico, medicamentos: list[str]):
        self._validar_parametros(paciente, medico, medicamentos)
        
        self.__paciente = paciente
        self.__medico = medico
        self.__medicamentos = [med.strip() for med in medicamentos if med.strip()]
        self.__fecha = datetime.now()

    def _validar_parametros(self, paciente, medico, medicamentos):
        """Valida que todos los parámetros sean válidos."""
        if paciente is None:
            raise DatosInvalidosException("El paciente no puede ser None")
        
        if medico is None:
            raise DatosInvalidosException("El médico no puede ser None")
        
        if not medicamentos or len(medicamentos) == 0:
            raise RecetaInvalidaException("Debe especificar al menos un medicamento")
        
        medicamentos_validos = [med for med in medicamentos if med and med.strip()]
        if len(medicamentos_validos) == 0:
            raise RecetaInvalidaException("Todos los medicamentos están vacíos")

    def obtener_paciente(self):
        return self.__paciente

    def obtener_medico(self):
        return self.__medico

    def obtener_medicamentos(self) -> list[str]:
        return self.__medicamentos.copy()

    def obtener_fecha(self) -> datetime:
        return self.__fecha

    def _str_(self) -> str:
        medicamentos_str = ', '.join(self.__medicamentos)
        fecha_str = self.__fecha.strftime("%d/%m/%Y %H:%M")
        return f"Receta: {self._paciente.obtener_nombre()}, Dr. {self._medico.obtener_nombre()}, Medicamentos: {medicamentos_str}, Fecha: {fecha_str}"
