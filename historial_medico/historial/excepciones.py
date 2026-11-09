"""Excepciones del sistema de historial médico."""


class HistorialError(Exception):
    """Error base del sistema."""


class DatoInvalidoError(HistorialError):
    """Valor de entrada inválido para un atributo."""


class EntidadDuplicadaError(HistorialError):
    """Ya existe una entidad con la misma clave."""


class EntidadNoEncontradaError(HistorialError):
    """No existe una entidad con la clave indicada."""


class ReporteError(HistorialError):
    """Falla al generar o escribir el reporte PDF."""
