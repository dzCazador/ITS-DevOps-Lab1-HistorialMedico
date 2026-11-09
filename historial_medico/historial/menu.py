"""Menú interactivo de consola para el sistema de historial médico."""

from historial.excepciones import DatoInvalidoError, HistorialError
from historial.personas import Medico, Paciente
from historial.reportes import generar_reporte_pdf

_TIPOS_ATENCION = ("consulta", "urgencia", "control")
_RUTA_PDF_DEFECTO = "reporte.pdf"

_MENU_TEXTO = """
==== Historial médico ====
1. Registrar médico
2. Registrar paciente
3. Registrar atención
4. Listar médicos
5. Listar pacientes
6. Ver historial de un paciente
7. Ver facturación de un médico
8. Guardar reporte PDF
0. Salir
"""

_OPCIONES = ("0", "1", "2", "3", "4", "5", "6", "7", "8")


class Menu:
    """Menú de consola con entrada y salida inyectables."""

    def __init__(self, repositorio, entrada=input, salida=print):
        self.__repositorio = repositorio
        self.__entrada = entrada
        self.__salida = salida
        self.__acciones = {
            "1": self.__registrar_medico,
            "2": self.__registrar_paciente,
            "3": self.__registrar_atencion,
            "4": self.__listar_medicos,
            "5": self.__listar_pacientes,
            "6": self.__ver_historial,
            "7": self.__ver_facturacion,
            "8": self.__guardar_pdf,
        }

    def mostrar_menu(self):
        """Muestra las opciones disponibles."""
        self.__salida(_MENU_TEXTO)

    def leer_opcion(self):
        """Pide una opción válida hasta que el usuario ingrese una de la lista."""
        while True:
            opcion = self.__entrada("Seleccione una opción: ").strip()
            if opcion in _OPCIONES:
                return opcion
            self.__salida(f"Opción inválida: {opcion!r}. Ingrese un número del menú.")

    def ejecutar(self):
        """Ejecuta el bucle principal hasta que se elige 0 (Salir)."""
        while True:
            self.mostrar_menu()
            opcion = self.leer_opcion()
            if opcion == "0":
                self.__salida("Saliendo del sistema.")
                return
            try:
                self.__acciones[opcion]()
            except (HistorialError, ValueError, TypeError) as exc:
                self.__salida(f"Error: {exc}")

    def __pedir(self, etiqueta):
        return self.__entrada(f"{etiqueta}: ").strip()

    def __registrar_medico(self):
        nombre = self.__pedir("Nombre")
        dni = self.__pedir("DNI")
        matricula = self.__pedir("Matrícula")
        especialidad = self.__pedir("Especialidad")
        self.__repositorio.agregar_medico(Medico(nombre, dni, matricula, especialidad))
        self.__salida("Médico registrado.")

    def __registrar_paciente(self):
        nombre = self.__pedir("Nombre")
        dni = self.__pedir("DNI")
        fecha_nacimiento = self.__pedir("Fecha de nacimiento (YYYY-MM-DD)")
        self.__repositorio.agregar_paciente(Paciente(nombre, dni, fecha_nacimiento))
        self.__salida("Paciente registrado.")

    def __registrar_atencion(self):
        dni = self.__pedir("DNI del paciente")
        matricula = self.__pedir("Matrícula del médico")
        fecha = self.__pedir("Fecha (YYYY-MM-DD)")
        tipo = self.__pedir("Tipo (consulta/urgencia/control)").lower()
        if tipo not in _TIPOS_ATENCION:
            raise DatoInvalidoError("tipo debe ser consulta, urgencia o control")
        atencion = self.__repositorio.registrar_atencion(dni, matricula, fecha, tipo)
        self.__salida(f"Atención registrada: {atencion.descripcion()}")

    def __listar_medicos(self):
        medicos = self.__repositorio.listar_medicos()
        if not medicos:
            self.__salida("No hay médicos registrados.")
        for medico in medicos:
            self.__salida(medico.descripcion())

    def __listar_pacientes(self):
        pacientes = self.__repositorio.listar_pacientes()
        if not pacientes:
            self.__salida("No hay pacientes registrados.")
        for paciente in pacientes:
            self.__salida(paciente.descripcion())

    def __ver_historial(self):
        dni = self.__pedir("DNI del paciente")
        atenciones = self.__repositorio.historial_paciente(dni)
        if not atenciones:
            self.__salida("El paciente no tiene atenciones registradas.")
        for atencion in atenciones:
            self.__salida(atencion.descripcion())

    def __ver_facturacion(self):
        matricula = self.__pedir("Matrícula del médico")
        total = self.__repositorio.facturacion_medico(matricula)
        self.__salida(f"Facturación total: {total:.2f}")

    def __guardar_pdf(self):
        ruta = self.__pedir(f"Ruta del archivo [{_RUTA_PDF_DEFECTO}]") or _RUTA_PDF_DEFECTO
        generar_reporte_pdf(self.__repositorio, ruta)
        self.__salida(f"Reporte guardado en {ruta}.")
