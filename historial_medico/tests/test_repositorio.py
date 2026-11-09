"""Tests del repositorio en memoria del historial médico."""

import pytest

from historial.atenciones import COSTO_CONSULTA, COSTO_URGENCIA
from historial.excepciones import (
    DatoInvalidoError,
    EntidadDuplicadaError,
    EntidadNoEncontradaError,
)
from historial.personas import Medico, Paciente
from historial.repositorio import RepositorioHistorial


def _medico(matricula="1001", dni="30111222"):
    return Medico("Ana Gómez", dni, matricula, "clínica")


def _paciente(dni="40111222"):
    return Paciente("Luis Pérez", dni, "1990-05-10")


@pytest.fixture
def repo():
    return RepositorioHistorial()


def test_agregar_medico_y_buscar(repo):
    m = _medico()
    repo.agregar_medico(m)
    assert repo.buscar_medico("1001") is m


def test_agregar_medico_duplicado_lanza_error(repo):
    repo.agregar_medico(_medico())
    with pytest.raises(EntidadDuplicadaError):
        repo.agregar_medico(_medico(dni="30999999"))


def test_agregar_medico_tipo_invalido_lanza_error(repo):
    with pytest.raises(DatoInvalidoError):
        repo.agregar_medico(_paciente())


def test_buscar_medico_inexistente_lanza_error(repo):
    with pytest.raises(EntidadNoEncontradaError):
        repo.buscar_medico("9999")


def test_agregar_paciente_y_buscar(repo):
    p = _paciente()
    repo.agregar_paciente(p)
    assert repo.buscar_paciente("40111222") is p


def test_agregar_paciente_duplicado_lanza_error(repo):
    repo.agregar_paciente(_paciente())
    with pytest.raises(EntidadDuplicadaError):
        repo.agregar_paciente(_paciente())


def test_agregar_paciente_tipo_invalido_lanza_error(repo):
    with pytest.raises(DatoInvalidoError):
        repo.agregar_paciente(_medico())


def test_buscar_paciente_inexistente_lanza_error(repo):
    with pytest.raises(EntidadNoEncontradaError):
        repo.buscar_paciente("00000000")


def test_registrar_atencion_crea_y_guarda(repo):
    repo.agregar_paciente(_paciente())
    repo.agregar_medico(_medico())
    at = repo.registrar_atencion("40111222", "1001", "2026-01-10", "urgencia")
    assert at.tipo() == "urgencia"
    assert at.costo() == COSTO_URGENCIA
    assert repo.listar_atenciones() == [at]


def test_registrar_atencion_paciente_inexistente(repo):
    repo.agregar_medico(_medico())
    with pytest.raises(EntidadNoEncontradaError):
        repo.registrar_atencion("40111222", "1001", "2026-01-10", "consulta")


def test_registrar_atencion_medico_inexistente(repo):
    repo.agregar_paciente(_paciente())
    with pytest.raises(EntidadNoEncontradaError):
        repo.registrar_atencion("40111222", "1001", "2026-01-10", "consulta")


def test_registrar_atencion_tipo_invalido(repo):
    repo.agregar_paciente(_paciente())
    repo.agregar_medico(_medico())
    with pytest.raises(DatoInvalidoError):
        repo.registrar_atencion("40111222", "1001", "2026-01-10", "cirugia")


def test_historial_paciente_ordenado_por_fecha(repo):
    repo.agregar_paciente(_paciente())
    repo.agregar_medico(_medico())
    tarde = repo.registrar_atencion("40111222", "1001", "2026-03-01", "consulta")
    temprano = repo.registrar_atencion("40111222", "1001", "2026-01-01", "control")
    assert repo.historial_paciente("40111222") == [temprano, tarde]


def test_historial_paciente_solo_sus_atenciones(repo):
    repo.agregar_paciente(_paciente())
    repo.agregar_paciente(_paciente(dni="40999999"))
    repo.agregar_medico(_medico())
    propia = repo.registrar_atencion("40111222", "1001", "2026-01-01", "consulta")
    repo.registrar_atencion("40999999", "1001", "2026-01-02", "consulta")
    assert repo.historial_paciente("40111222") == [propia]


def test_historial_paciente_inexistente_lanza_error(repo):
    with pytest.raises(EntidadNoEncontradaError):
        repo.historial_paciente("00000000")


def test_facturacion_medico_suma_costos(repo):
    repo.agregar_paciente(_paciente())
    repo.agregar_medico(_medico())
    repo.registrar_atencion("40111222", "1001", "2026-01-01", "urgencia")
    repo.registrar_atencion("40111222", "1001", "2026-01-02", "consulta")
    total = repo.facturacion_medico("1001")
    assert isinstance(total, float)
    assert total == COSTO_URGENCIA + COSTO_CONSULTA


def test_facturacion_medico_sin_atenciones_es_cero(repo):
    repo.agregar_medico(_medico())
    assert repo.facturacion_medico("1001") == 0.0


def test_facturacion_medico_inexistente_lanza_error(repo):
    with pytest.raises(EntidadNoEncontradaError):
        repo.facturacion_medico("9999")


def test_listar_devuelve_copias(repo):
    repo.agregar_medico(_medico())
    repo.agregar_paciente(_paciente())
    repo.registrar_atencion("40111222", "1001", "2026-01-01", "consulta")

    medicos = repo.listar_medicos()
    pacientes = repo.listar_pacientes()
    atenciones = repo.listar_atenciones()
    medicos.clear()
    pacientes.clear()
    atenciones.clear()

    assert len(repo.listar_medicos()) == 1
    assert len(repo.listar_pacientes()) == 1
    assert len(repo.listar_atenciones()) == 1


def test_historial_paciente_devuelve_copia(repo):
    repo.agregar_paciente(_paciente())
    repo.agregar_medico(_medico())
    repo.registrar_atencion("40111222", "1001", "2026-01-01", "consulta")
    historial = repo.historial_paciente("40111222")
    historial.clear()
    assert len(repo.historial_paciente("40111222")) == 1
