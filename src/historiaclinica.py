class HistoriaClinica:
    def __init__(self, paciente):
        self.__paciente = paciente
        self.__turnos = []
        self.__recetas = []
    
    def agregar_turno(self, turno):
        self.__turnos.append(turno)
      
    
    def agregar_receta(self, receta):
        self.__recetas.append(receta)
        
    
    def obtener_paciente(self):
        return self.__paciente
    
    def obtener_turnos(self) -> list:
        return self.__turnos.copy()
    
    def obtener_recetas(self) -> list:
        return self.__recetas.copy()
    
    def _str_(self) -> str:
        turnos_str = '\n'.join(str(t) for t in self.__turnos)
        recetas_str = '\n'.join(str(r) for r in self.__recetas)
        return f"Historia Clínica de {self.__paciente}:\nTurnos:\n{turnos_str}\nRecetas:\n{recetas_str}"
    
