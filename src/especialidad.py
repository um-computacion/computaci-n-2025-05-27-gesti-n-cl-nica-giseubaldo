class Especialidad:
    def __init__(self, tipo, dias):
        self._tipo = tipo
        self._dias = [dia.lower() for dia in dias]
    
    def obtener_especialidad(self):
        return self._tipo
    
    def verificar_dia(self, dia):
        return dia.lower() in self._dias
    
    def __str__(self):
        dias_str = ", ".join(self._dias)
        return f"{self._tipo} (Días: {dias_str})"
    
    