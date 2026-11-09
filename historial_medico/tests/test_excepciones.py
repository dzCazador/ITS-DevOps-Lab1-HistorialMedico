import pytest

from historial.excepciones import DatoInvalidoError, HistorialError


def test_historial_error_es_exception():
    assert issubclass(HistorialError, Exception)


def test_dato_invalido_error_hereda_de_historial_error():
    assert issubclass(DatoInvalidoError, HistorialError)


def test_dato_invalido_error_se_puede_capturar_como_base():
    with pytest.raises(HistorialError):
        raise DatoInvalidoError("valor inválido")
