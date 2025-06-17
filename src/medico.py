class Medico:

    def __init__(self, nombre, matricula):
        self._nombre = nombre
        self._matricula = matricula
        self._especialidades = []
    
    def agregar_especialidad(self, especialidad):
        self._especialidades.append(especialidad)
    
    def obtener_matricula(self):
        return self._matricula
    
    def obtener_especialidad_para_dia(self, dia):
        for especialidad in self._especialidades:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_especialidad()
        return None
    
    def __str__(self):
        especialidades_str = [str(esp) for esp in self._especialidades]
        if especialidades_str:
            especialidades_texto = "; ".join(especialidades_str)
            return f"Dr. {self._nombre} - Matrícula: {self._matricula} - Especialidades: {especialidades_texto}"
        else:
            return f"Dr. {self._nombre} - Matrícula: {self._matricula} - Sin especialidades"


