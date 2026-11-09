"""Excepciones del sistema de historial médico."""


class HistorialError(Exception):
    """Error base del sistema."""


class DatoInvalidoError(HistorialError):
    """Valor de entrada inválido para un atributo."""
