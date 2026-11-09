"""Clases de personas: Persona (abstracta), Medico y Paciente."""

import re
from abc import ABC, abstractmethod
from datetime import datetime

from historial.excepciones import DatoInvalidoError

_PATRON_SOLO_DIGITOS = re.compile(r"^[0-9]+$")
_PATRON_DNI = re.compile(r"^[0-9]{8}$")
_PATRON_FECHA = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


def _validar_texto_no_vacio(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise DatoInvalidoError(f"{campo} debe ser un texto no vacío")
    return valor


class Persona(ABC):
    """Base abstracta para personas del sistema."""

    def __init__(self, nombre, dni):
        self.__nombre = None
        self.__dni = None
        self.nombre = nombre
        self.dni = dni

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = _validar_texto_no_vacio(valor, "nombre")

    @property
    def dni(self):
        return self.__dni

    @dni.setter
    def dni(self, valor):
        if not isinstance(valor, str) or not _PATRON_DNI.match(valor):
            raise DatoInvalidoError("dni debe tener exactamente 8 dígitos")
        self.__dni = valor

    @abstractmethod
    def descripcion(self):
        """Devuelve una descripción textual de la persona."""


class Medico(Persona):
    """Médico con matrícula y especialidad."""

    def __init__(self, nombre, dni, matricula, especialidad):
        super().__init__(nombre, dni)
        self.__matricula = None
        self.__especialidad = None
        self.matricula = matricula
        self.especialidad = especialidad

    @property
    def matricula(self):
        return self.__matricula

    @matricula.setter
    def matricula(self, valor):
        if not isinstance(valor, str) or not _PATRON_SOLO_DIGITOS.match(valor):
            raise DatoInvalidoError("matricula debe contener solo dígitos")
        self.__matricula = valor

    @property
    def especialidad(self):
        return self.__especialidad

    @especialidad.setter
    def especialidad(self, valor):
        self.__especialidad = _validar_texto_no_vacio(valor, "especialidad")

    def descripcion(self):
        return (
            f"Médico: {self.nombre} (DNI {self.dni}), "
            f"matrícula {self.matricula}, especialidad {self.especialidad}"
        )


class Paciente(Persona):
    """Paciente con fecha de nacimiento en formato YYYY-MM-DD."""

    def __init__(self, nombre, dni, fecha_nacimiento):
        super().__init__(nombre, dni)
        self.__fecha_nacimiento = None
        self.fecha_nacimiento = fecha_nacimiento

    @property
    def fecha_nacimiento(self):
        return self.__fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, valor):
        if not isinstance(valor, str) or not _PATRON_FECHA.match(valor):
            raise DatoInvalidoError("fecha_nacimiento debe tener formato YYYY-MM-DD")
        try:
            datetime.strptime(valor, "%Y-%m-%d")
        except ValueError as exc:
            raise DatoInvalidoError("fecha_nacimiento no es una fecha válida") from exc
        self.__fecha_nacimiento = valor

    def descripcion(self):
        return (
            f"Paciente: {self.nombre} (DNI {self.dni}), "
            f"nacimiento {self.fecha_nacimiento}"
        )
