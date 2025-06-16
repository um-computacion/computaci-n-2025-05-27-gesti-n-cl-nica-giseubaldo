class Paciente:
    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):
        self.__nombre = nombre
        self.__dni = dni
        self.__fecha_nacimiento = fecha_nacimiento

    def obtener_dni(self) -> str:
        return self.__dni

    def __str__(self) -> str:
        return f"Paciente: {self.__nombre} - DNI: {self.__dni} - Nacimiento: {self.__fecha_nacimiento}"

