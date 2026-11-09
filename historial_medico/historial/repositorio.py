"""Repositorio en memoria para médicos, pacientes y atenciones."""

from historial.atenciones import crear_atencion
from historial.excepciones import (
    DatoInvalidoError,
    EntidadDuplicadaError,
    EntidadNoEncontradaError,
)
from historial.personas import Medico, Paciente


class RepositorioHistorial:
    """Almacena médicos, pacientes y atenciones en listas internas."""

    def __init__(self):
        self.__medicos = []
        self.__pacientes = []
        self.__atenciones = []

    def agregar_medico(self, medico):
        """Agrega un médico; falla si la matrícula ya existe o el tipo es inválido."""
        if not isinstance(medico, Medico):
            raise DatoInvalidoError("medico debe ser una instancia de Medico")
        if any(m.matricula == medico.matricula for m in self.__medicos):
            raise EntidadDuplicadaError(f"ya existe un médico con matrícula {medico.matricula}")
        self.__medicos.append(medico)

    def agregar_paciente(self, paciente):
        """Agrega un paciente; falla si el DNI ya existe o el tipo es inválido."""
        if not isinstance(paciente, Paciente):
            raise DatoInvalidoError("paciente debe ser una instancia de Paciente")
        if any(p.dni == paciente.dni for p in self.__pacientes):
            raise EntidadDuplicadaError(f"ya existe un paciente con DNI {paciente.dni}")
        self.__pacientes.append(paciente)

    def buscar_medico(self, matricula):
        """Devuelve el médico con la matrícula indicada."""
        for medico in self.__medicos:
            if medico.matricula == matricula:
                return medico
        raise EntidadNoEncontradaError(f"no existe médico con matrícula {matricula}")

    def buscar_paciente(self, dni):
        """Devuelve el paciente con el DNI indicado."""
        for paciente in self.__pacientes:
            if paciente.dni == dni:
                return paciente
        raise EntidadNoEncontradaError(f"no existe paciente con DNI {dni}")

    def registrar_atencion(self, dni, matricula, fecha, tipo):
        """Crea y guarda una atención entre un paciente y un médico existentes."""
        paciente = self.buscar_paciente(dni)
        medico = self.buscar_medico(matricula)
        atencion = crear_atencion(tipo, paciente, medico, fecha)
        self.__atenciones.append(atencion)
        return atencion

    def historial_paciente(self, dni):
        """Devuelve las atenciones del paciente ordenadas por fecha."""
        paciente = self.buscar_paciente(dni)
        propias = [a for a in self.__atenciones if a.paciente is paciente]
        return sorted(propias, key=lambda a: a.fecha)

    def facturacion_medico(self, matricula):
        """Suma el costo de las atenciones del médico indicado."""
        medico = self.buscar_medico(matricula)
        total = sum(a.costo() for a in self.__atenciones if a.medico is medico)
        return float(total)

    def listar_medicos(self):
        """Devuelve una copia de la lista de médicos."""
        return list(self.__medicos)

    def listar_pacientes(self):
        """Devuelve una copia de la lista de pacientes."""
        return list(self.__pacientes)

    def listar_atenciones(self):
        """Devuelve una copia de la lista de atenciones."""
        return list(self.__atenciones)
