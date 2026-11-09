import pytest

from historial.atenciones import (
    COSTO_CONSULTA,
    COSTO_CONTROL,
    COSTO_URGENCIA,
    Atencion,
    AtencionConsulta,
    Control,
    Urgencia,
    crear_atencion,
)
from historial.excepciones import DatoInvalidoError
from historial.personas import Medico, Paciente


def _paciente():
    return Paciente("Ana", "12345678", "1990-05-10")


def _medico():
    return Medico("Dr. House", "87654321", "12345", "Clínica")


FECHA = "2026-03-15"


def test_atencion_no_se_puede_instanciar_por_ser_abstracta():
    with pytest.raises(TypeError):
        Atencion(_paciente(), _medico(), FECHA)


def test_consulta_tipo_costo_y_descripcion():
    a = AtencionConsulta(_paciente(), _medico(), FECHA)
    assert a.tipo() == "consulta"
    assert a.costo() == 12000.0 == COSTO_CONSULTA
    assert a.descripcion() == f"consulta {FECHA} - costo 12000.0"


def test_urgencia_tipo_costo_y_descripcion():
    a = Urgencia(_paciente(), _medico(), FECHA)
    assert a.tipo() == "urgencia"
    assert a.costo() == 18000.0 == COSTO_URGENCIA
    assert a.descripcion() == f"urgencia {FECHA} - costo 18000.0"


def test_control_tipo_costo_y_descripcion():
    a = Control(_paciente(), _medico(), FECHA)
    assert a.tipo() == "control"
    assert a.costo() == 6000.0 == COSTO_CONTROL
    assert a.descripcion() == f"control {FECHA} - costo 6000.0"


def test_getters_devuelven_los_valores_asignados():
    p, m = _paciente(), _medico()
    a = Control(p, m, FECHA)
    assert a.paciente is p
    assert a.medico is m
    assert a.fecha == FECHA


def test_polimorfismo_sobre_lista_mixta():
    atenciones = [
        AtencionConsulta(_paciente(), _medico(), FECHA),
        Urgencia(_paciente(), _medico(), FECHA),
        Control(_paciente(), _medico(), FECHA),
    ]
    assert [a.tipo() for a in atenciones] == ["consulta", "urgencia", "control"]
    assert sum(a.costo() for a in atenciones) == 36000.0
    assert all(isinstance(a, Atencion) for a in atenciones)


@pytest.mark.parametrize("fecha", ["2026-02-30", "15-03-2026", "2026/03/15", "", None, 20260315])
def test_fecha_invalida_lanza_error(fecha):
    with pytest.raises(DatoInvalidoError):
        Control(_paciente(), _medico(), fecha)


def test_setter_fecha_valida_y_rechaza_invalida():
    a = Control(_paciente(), _medico(), FECHA)
    a.fecha = "2026-12-31"
    assert a.fecha == "2026-12-31"
    with pytest.raises(DatoInvalidoError):
        a.fecha = "2026-13-01"
    assert a.fecha == "2026-12-31"


def test_paciente_debe_ser_paciente():
    with pytest.raises(DatoInvalidoError):
        Control(_medico(), _medico(), FECHA)
    with pytest.raises(DatoInvalidoError):
        Control("Ana", _medico(), FECHA)


def test_medico_debe_ser_medico():
    with pytest.raises(DatoInvalidoError):
        Control(_paciente(), _paciente(), FECHA)
    with pytest.raises(DatoInvalidoError):
        Control(_paciente(), None, FECHA)


def test_setters_de_paciente_y_medico_validan_tipo():
    a = Control(_paciente(), _medico(), FECHA)
    with pytest.raises(DatoInvalidoError):
        a.paciente = _medico()
    with pytest.raises(DatoInvalidoError):
        a.medico = _paciente()


def test_factory_crea_cada_tipo():
    p, m = _paciente(), _medico()
    assert isinstance(crear_atencion("consulta", p, m, FECHA), AtencionConsulta)
    assert isinstance(crear_atencion("urgencia", p, m, FECHA), Urgencia)
    assert isinstance(crear_atencion("control", p, m, FECHA), Control)


def test_factory_tipo_desconocido_lanza_error():
    with pytest.raises(DatoInvalidoError):
        crear_atencion("cirugia", _paciente(), _medico(), FECHA)
