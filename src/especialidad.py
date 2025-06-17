from .excepciones import DatosInvalidosException
class Especialidad:
    DIAS_VALIDOS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    
    def _init_(self, tipo: str, dias: list[str]):
        self._validar_tipo(tipo)
        self._validar_dias(dias)
        
        self.__tipo = tipo.strip()
        self.__dias = [d.lower().strip() for d in dias]

    def _validar_tipo(self, tipo: str):
        """Valida que el tipo de especialidad no esté vacío."""
        if not tipo or not tipo.strip():
            raise DatosInvalidosException("El tipo de especialidad no puede estar vacío")

    def _validar_dias(self, dias: list[str]):
        """Valida que los días sean válidos y no estén duplicados."""
        if not dias or len(dias) == 0:
            raise DatosInvalidosException("Debe especificar al menos un día de atención")
        
        dias_normalizados = []
        for dia in dias:
            if not dia or not dia.strip():
                raise DatosInvalidosException("Los días no pueden estar vacíos")
            
            dia_normalizado = dia.lower().strip()
            if dia_normalizado not in self.DIAS_VALIDOS:
                raise DatosInvalidosException(f"'{dia}' no es un día válido. Días válidos: {', '.join(self.DIAS_VALIDOS)}")
            
            if dia_normalizado in dias_normalizados:
                raise DatosInvalidosException(f"El día '{dia}' está duplicado")
            
            dias_normalizados.append(dia_normalizado)

    def obtener_especialidad(self) -> str:
        return self.__tipo

    def verificar_dia(self, dia: str) -> bool:
        if not dia:
            return False
        return dia.lower().strip() in self.__dias

    def obtener_dias(self) -> list[str]:
        return self.__dias.copy()

    def _str_(self) -> str:
        dias_str = ', '.join(self.__dias)
        return f"{self.__tipo} (Días: {dias_str})"
    