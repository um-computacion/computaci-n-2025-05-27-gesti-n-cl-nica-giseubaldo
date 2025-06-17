class Medico:
    def __init__(self, nombre, especialidad, matricula):
        self._nombre = nombre
        self._especialidad = especialidad
        self._matricula = matricula

    def obtener_matricula(self):
        return self._matricula

    def __str__(self):
        return f"Dr: {self._nombre} - Especialidad: {self._especialidad} - Matricula: {self._matricula}"


