class Turno:
    def __init__(self, paciente, medico, fecha_hora, especialidad):
        self._paciente = paciente
        self._medico = medico
        self._fecha_hora = fecha_hora
        self._especialidad = especialidad
    
    def obtener_medico(self):
        return self._medico
    
    def obtener_fecha_hora(self):
        return self._fecha_hora
    
    def __str__(self):
        fecha_str = self._fecha_hora.strftime("%d/%m/%Y %H:%M")
        return (f"Turno - Paciente: {self._paciente.obtener_nombre()} | "
                f"Médico: Dr. {self._medico._nombre} | "
                f"Especialidad: {self._especialidad} | "
                f"Fecha: {fecha_str}")
