from datetime import datetime
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clinica import Clinica
from paciente import Paciente
from medico import Medico
from especialidad import Especialidad
from excepciones import (
    PacienteNoEncontradoException,
    MedicoNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    RecetaInvalidaException,
    PacienteDuplicadoException,
    MedicoDuplicadoException,
    EspecialidadDuplicadaException,
    DatosInvalidosException
)


class CLI:
    def __init__(self):
        self.clinica = Clinica()

    def mostrar_menu(self):
        """Muestra el menú principal."""
        print("\n" + "="*50)
        print("SISTEMA DE GESTION CLINICA")
        print("="*50)
        print("1) Agregar paciente")
        print("2) Agregar médico")
        print("3) Agendar turno")
        print("4) Agregar especialidad a médico")
        print("5) Emitir receta")
        print("6) Ver historia clínica")
        print("7) Ver todos los turnos")
        print("8) Ver todos los pacientes")
        print("9) Ver todos los médicos")
        print("0) Salir")
        print("="*50)

    def ejecutar(self):
        """Ejecuta el bucle principal de la CLI."""
        print("Bienvenido al Sistema de Gestión Clínica!")
        
        while True:
            try:
                self.mostrar_menu()
                opcion = input("Seleccione una opción: ").strip()
                
                if opcion == "0":
                    print("Gracias por usar el sistema! Hasta luego!")
                    break
                elif opcion == "1":
                    self.agregar_paciente()
                elif opcion == "2":
                    self.agregar_medico()
                elif opcion == "3":
                    self.agendar_turno()
                elif opcion == "4":
                    self.agregar_especialidad()
                elif opcion == "5":
                    self.emitir_receta()
                elif opcion == "6":
                    self.ver_historia_clinica()
                elif opcion == "7":
                    self.ver_turnos()
                elif opcion == "8":
                    self.ver_pacientes()
                elif opcion == "9":
                    self.ver_medicos()
                else:
                    print("ERROR: Opción inválida. Por favor, seleccione una opción válida.")
                    
            except KeyboardInterrupt:
                print("\n\nHasta luego!")
                break
            except Exception as e:
                print(f"ERROR: Error inesperado: {e}")

    def agregar_paciente(self):
        """Solicita datos y agrega un paciente."""
        print("\nAGREGAR PACIENTE")
        print("-" * 30)
        
        try:
            nombre = input("Nombre completo: ").strip()
            dni = input("DNI: ").strip()
            fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ").strip()
            
            paciente = Paciente(nombre, dni, fecha_nacimiento)
            self.clinica.agregar_paciente(paciente)
            
            print(f"OK: Paciente {nombre} registrado exitosamente.")
            
        except (DatosInvalidosException, PacienteDuplicadoException) as e:
            print(f"ERROR: {e}")

    def agregar_medico(self):
        """Solicita datos y agrega un médico."""
        print("\nAGREGAR MEDICO")
        print("-" * 30)
        
        try:
            nombre = input("Nombre completo: ").strip()
            matricula = input("Matrícula: ").strip()
            
            medico = Medico(nombre, matricula)
            
            # Preguntar si quiere agregar especialidades ahora
            agregar_esp = input("¿Desea agregar especialidades ahora? (s/n): ").strip().lower()
            
            if agregar_esp == 's':
                self._agregar_especialidades_interactivo(medico)
            
            self.clinica.agregar_medico(medico)
            print(f"OK: Médico Dr. {nombre} registrado exitosamente.")
            
        except (DatosInvalidosException, MedicoDuplicadoException, EspecialidadDuplicadaException) as e:
            print(f"ERROR: {e}")

    def _agregar_especialidades_interactivo(self, medico):
        """Agrega especialidades a un médico de forma interactiva."""
        while True:
            try:
                print("\nAgregando especialidad:")
                tipo = input("Tipo de especialidad: ").strip()
                if not tipo:
                    break
                
                print("Días de atención (separados por comas):")
                print("Ejemplo: lunes,miércoles,viernes")
                dias_str = input("Días: ").strip()
                
                if not dias_str:
                    break
                
                dias = [dia.strip() for dia in dias_str.split(',')]
                especialidad = Especialidad(tipo, dias)
                medico.agregar_especialidad(especialidad)
                
                print(f"OK: Especialidad {tipo} agregada.")
                
                continuar = input("¿Agregar otra especialidad? (s/n): ").strip().lower()
                if continuar != 's':
                    break
                    
            except (DatosInvalidosException, EspecialidadDuplicadaException) as e:
                print(f"ERROR: {e}")

    def agregar_especialidad(self):
        """Agrega una especialidad a un médico existente."""
        print("\nAGREGAR ESPECIALIDAD A MEDICO")
        print("-" * 40)
        
        try:
            # Mostrar médicos disponibles
            medicos = self.clinica.obtener_medicos()
            if not medicos:
                print("ERROR: No hay médicos registrados.")
                return
            
            print("Médicos disponibles:")
            for i, medico in enumerate(medicos, 1):
                print(f"{i}) Dr. {medico.obtener_nombre()} - Matrícula: {medico.obtener_matricula()}")
            
            matricula = input("\nMatrícula del médico: ").strip()
            medico = self.clinica.obtener_medico_por_matricula(matricula)
            
            tipo = input("Tipo de especialidad: ").strip()
            print("Días de atención (separados por comas):")
            print("Ejemplo: lunes,miércoles,viernes")
            dias_str = input("Días: ").strip()
            
            dias = [dia.strip() for dia in dias_str.split(',')]
            especialidad = Especialidad(tipo, dias)
            medico.agregar_especialidad(especialidad)
            
            print(f"OK: Especialidad {tipo} agregada al Dr. {medico.obtener_nombre()}.")
            
        except (MedicoNoEncontradoException, DatosInvalidosException, EspecialidadDuplicadaException) as e:
            print(f"ERROR: {e}")

    def agendar_turno(self):
        """Agenda un turno."""
        print("\nAGENDAR TURNO")
        print("-" * 25)
        
        try:
            # Mostrar pacientes
            pacientes = self.clinica.obtener_pacientes()
            if not pacientes:
                print("ERROR: No hay pacientes registrados.")
                return
            
            print("Pacientes disponibles:")
            for paciente in pacientes:
                print(f"- {paciente.obtener_nombre()} (DNI: {paciente.obtener_dni()})")
            
            dni = input("\nDNI del paciente: ").strip()
            
            # Mostrar médicos
            medicos = self.clinica.obtener_medicos()
            if not medicos:
                print("ERROR: No hay médicos registrados.")
                return
            
            print("\nMédicos disponibles:")
            for medico in medicos:
                print(f"- Dr. {medico.obtener_nombre()} (Matrícula: {medico.obtener_matricula()})")
                especialidades = medico.obtener_especialidades()
                for esp in especialidades:
                    print(f"  * {esp}")
            
            matricula = input("\nMatrícula del médico: ").strip()
            especialidad = input("Especialidad: ").strip()
            
            # Solicitar fecha y hora
            fecha_str = input("Fecha (dd/mm/aaaa): ").strip()
            hora_str = input("Hora (HH:MM): ").strip()
            
            # Convertir a datetime
            fecha_hora_str = f"{fecha_str} {hora_str}"
            fecha_hora = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M")
            
            self.clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)
            print("OK: Turno agendado exitosamente.")
            
        except (PacienteNoEncontradoException, MedicoNoEncontradoException, 
                MedicoNoDisponibleException, TurnoOcupadoException, DatosInvalidosException) as e:
            print(f"ERROR: {e}")
        except ValueError:
            print("ERROR: Formato de fecha u hora inválido.")

    def emitir_receta(self):
        """Emite una receta médica."""
        print("\nEMITIR RECETA")
        print("-" * 25)
        
        try:
            # Mostrar pacientes
            pacientes = self.clinica.obtener_pacientes()
            if not pacientes:
                print("ERROR: No hay pacientes registrados.")
                return
            
            print("Pacientes disponibles:")
            for paciente in pacientes:
                print(f"- {paciente.obtener_nombre()} (DNI: {paciente.obtener_dni()})")
            
            dni = input("\nDNI del paciente: ").strip()
            
            # Mostrar médicos
            medicos = self.clinica.obtener_medicos()
            if not medicos:
                print("ERROR: No hay médicos registrados.")
                return
            
            print("\nMédicos disponibles:")
            for medico in medicos:
                print(f"- Dr. {medico.obtener_nombre()} (Matrícula: {medico.obtener_matricula()})")
            
            matricula = input("\nMatrícula del médico: ").strip()
            
            print("Medicamentos (separados por comas):")
            medicamentos_str = input("Medicamentos: ").strip()
            medicamentos = [med.strip() for med in medicamentos_str.split(',')]
            
            self.clinica.emitir_receta(dni, matricula, medicamentos)
            print("OK: Receta emitida exitosamente.")
            
        except (PacienteNoEncontradoException, MedicoNoEncontradoException, 
                RecetaInvalidaException, DatosInvalidosException) as e:
            print(f"ERROR: {e}")

    def ver_historia_clinica(self):
        """Muestra la historia clínica de un paciente."""
        print("\nHISTORIA CLINICA")
        print("-" * 30)
        
        try:
            # Mostrar pacientes
            pacientes = self.clinica.obtener_pacientes()
            if not pacientes:
                print("ERROR: No hay pacientes registrados.")
                return
            
            print("Pacientes disponibles:")
            for paciente in pacientes:
                print(f"- {paciente.obtener_nombre()} (DNI: {paciente.obtener_dni()})")
            
            dni = input("\nDNI del paciente: ").strip()
            historia = self.clinica.obtener_historia_clinica(dni)
            
            print(f"\n{historia}")
            
        except PacienteNoEncontradoException as e:
            print(f"ERROR: {e}")

    def ver_turnos(self):
        """Muestra todos los turnos agendados."""
        print("\nTURNOS AGENDADOS")
        print("-" * 30)
        
        turnos = self.clinica.obtener_turnos()
        if not turnos:
            print("No hay turnos agendados.")
            return
        
        for i, turno in enumerate(turnos, 1):
            print(f"{i}) {turno}")

    def ver_pacientes(self):
        """Muestra todos los pacientes registrados."""
        print("\nPACIENTES REGISTRADOS")
        print("-" * 35)
        
        pacientes = self.clinica.obtener_pacientes()
        if not pacientes:
            print("No hay pacientes registrados.")
            return
        
        for i, paciente in enumerate(pacientes, 1):
            print(f"{i}) {paciente}")

    def ver_medicos(self):
        """Muestra todos los médicos registrados."""
        print("\nMEDICOS REGISTRADOS")
        print("-" * 35)
        
        medicos = self.clinica.obtener_medicos()
        if not medicos:
            print("No hay médicos registrados.")
            return
        
        for i, medico in enumerate(medicos, 1):
            print(f"{i}) {medico}")


def main():
    """Función principal para ejecutar la CLI."""
    cli = CLI()
    cli.ejecutar()


if __name__ == "__main__":
    main()