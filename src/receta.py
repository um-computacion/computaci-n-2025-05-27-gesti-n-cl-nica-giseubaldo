from datetime import datetime

class Receta:
    def __init__(self, paciente, medico, medicamentos):
        self._paciente = paciente
        self._medico = medico
        self._medicamentos = medicamentos
        self._fecha = datetime.now()
    
    def __str__(self):
        medicamentos_str = ", ".join(self._medicamentos)
        fecha_str = self._fecha.strftime("%d/%m/%Y")
        return (f"Receta - Paciente: {self._paciente.obtener_nombre()} | "
                f"Médico: Dr. {self._medico._nombre} | "
                f"Medicamentos: {medicamentos_str} | "
                f"Fecha: {fecha_str}")
