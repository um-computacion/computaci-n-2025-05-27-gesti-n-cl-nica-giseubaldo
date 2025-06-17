from datetime import datetime
from .excepciones import DatosInvalidosException

class Paciente:
    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):
        self._validar_nombre(nombre)
        self._validar_dni(dni)
        self._validar_fecha_nacimiento(fecha_nacimiento)
        
        self.__nombre = nombre.strip()
        self.__dni = dni.strip()
        self.__fecha_nacimiento = fecha_nacimiento

    def _validar_nombre(self, nombre: str):
        """Valida que el nombre no esté vacío y solo contenga letras, espacios y puntos."""
        if not nombre or not nombre.strip():
            raise DatosInvalidosException("El nombre no puede estar vacío")
        
        # Verificar que no contenga números
        if any(char.isdigit() for char in nombre):
            raise DatosInvalidosException("El nombre no puede contener números")
        
        # Quitar espacios y puntos para verificar que solo tenga letras
        nombre_solo_letras = nombre.replace(' ', '').replace('.', '')
        if not nombre_solo_letras.isalpha():
            raise DatosInvalidosException("El nombre solo puede contener letras, espacios y puntos")

    def _validar_dni(self, dni: str):
        """Valida que el DNI tenga el formato correcto."""
        if not dni or not dni.strip():
            raise DatosInvalidosException("El DNI no puede estar vacío")
        
        dni_limpio = dni.strip()
        if not (dni_limpio.isdigit() and 7 <= len(dni_limpio) <= 8):
            raise DatosInvalidosException("El DNI debe tener entre 7 y 8 dígitos")

    def _validar_fecha_nacimiento(self, fecha: str):
        """Valida que la fecha tenga el formato dd/mm/aaaa y sea válida."""
        if not fecha or not fecha.strip():
            raise DatosInvalidosException("La fecha de nacimiento no puede estar vacía")
        
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            raise DatosInvalidosException("La fecha debe tener formato dd/mm/aaaa y ser válida")

    def obtener_dni(self) -> str:
        return self.__dni

    def obtener_nombre(self) -> str:
        return self.__nombre

    def obtener_fecha_nacimiento(self) -> str:
        return self.__fecha_nacimiento

    def __str__(self) -> str:
        return f"{self.__nombre}, {self.__dni}, {self.__fecha_nacimiento}"