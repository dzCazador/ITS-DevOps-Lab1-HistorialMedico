"""Atenciones médicas: base abstracta Atencion y subclases con costo fijo."""

from abc import ABC, abstractmethod
from datetime import datetime

from historial.excepciones import DatoInvalidoError
from historial.personas import Medico, Paciente

COSTO_CONSULTA = 12000.0
COSTO_URGENCIA = 18000.0
COSTO_CONTROL = 6000.0


def _validar_fecha(valor):
    if not isinstance(valor, str):
        raise DatoInvalidoError("fecha debe tener formato YYYY-MM-DD")
    try:
        datetime.strptime(valor, "%Y-%m-%d")
    except ValueError as exc:
        raise DatoInvalidoError("fecha debe tener formato YYYY-MM-DD") from exc
    return valor


class Atencion(ABC):
    """Base abstracta para atenciones médicas."""

    def __init__(self, paciente, medico, fecha):
        self.__paciente = None
        self.__medico = None
        self.__fecha = None
        self.paciente = paciente
        self.medico = medico
        self.fecha = fecha

    @property
    def paciente(self):
        return self.__paciente

    @paciente.setter
    def paciente(self, valor):
        if not isinstance(valor, Paciente):
            raise DatoInvalidoError("paciente debe ser una instancia de Paciente")
        self.__paciente = valor

    @property
    def medico(self):
        return self.__medico

    @medico.setter
    def medico(self, valor):
        if not isinstance(valor, Medico):
            raise DatoInvalidoError("medico debe ser una instancia de Medico")
        self.__medico = valor

    @property
    def fecha(self):
        return self.__fecha

    @fecha.setter
    def fecha(self, valor):
        self.__fecha = _validar_fecha(valor)

    @abstractmethod
    def tipo(self):
        """Devuelve el nombre del tipo de atención."""

    @abstractmethod
    def costo(self):
        """Devuelve el costo de la atención."""

    def descripcion(self):
        """Devuelve una descripción textual de la atención."""
        return f"{self.tipo()} {self.fecha} - costo {self.costo()}"


class AtencionConsulta(Atencion):
    """Consulta médica general."""

    def tipo(self):
        return "consulta"

    def costo(self):
        return COSTO_CONSULTA


class Urgencia(Atencion):
    """Atención de urgencia."""

    def tipo(self):
        return "urgencia"

    def costo(self):
        return COSTO_URGENCIA


class Control(Atencion):
    """Control de seguimiento."""

    def tipo(self):
        return "control"

    def costo(self):
        return COSTO_CONTROL


_TIPOS = {
    "consulta": AtencionConsulta,
    "urgencia": Urgencia,
    "control": Control,
}


def crear_atencion(tipo, paciente, medico, fecha):
    """Crea una atención del tipo indicado; lanza DatoInvalidoError si el tipo no existe."""
    clase = _TIPOS.get(tipo)
    if clase is None:
        raise DatoInvalidoError(f"tipo de atención desconocido: {tipo!r}")
    return clase(paciente, medico, fecha)
