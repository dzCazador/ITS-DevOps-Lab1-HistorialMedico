import pytest

from historial.excepciones import DatoInvalidoError, HistorialError
from historial.personas import Medico, Paciente, Persona


class PersonaConcreta(Persona):
    def descripcion(self):
        return f"Persona: {self.nombre}"


def test_persona_no_se_puede_instanciar_por_ser_abstracta():
    with pytest.raises(TypeError):
        Persona("Ana", "12345678")


def test_persona_concreta_obtiene_nombre_y_dni():
    p = PersonaConcreta("Ana", "12345678")
    assert p.nombre == "Ana"
    assert p.dni == "12345678"


def test_atributos_privados_no_accesibles_directamente():
    p = PersonaConcreta("Ana", "12345678")
    assert not hasattr(p, "__nombre")
    assert not hasattr(p, "__dni")
    assert hasattr(p, "_Persona__nombre")
    assert hasattr(p, "_Persona__dni")


def test_setter_nombre_actualiza_valor():
    p = PersonaConcreta("Ana", "12345678")
    p.nombre = "Beatriz"
    assert p.nombre == "Beatriz"


@pytest.mark.parametrize("nombre", ["", "   ", None, 123])
def test_nombre_invalido_lanza_error(nombre):
    with pytest.raises(DatoInvalidoError):
        PersonaConcreta(nombre, "12345678")


def test_setter_nombre_invalido_lanza_error():
    p = PersonaConcreta("Ana", "12345678")
    with pytest.raises(DatoInvalidoError):
        p.nombre = ""


def test_setter_dni_actualiza_valor():
    p = PersonaConcreta("Ana", "12345678")
    p.dni = "87654321"
    assert p.dni == "87654321"


@pytest.mark.parametrize("dni", ["1234567", "123456789", "1234567A", "", "abcdefgh", None, 12345678])
def test_dni_invalido_lanza_error(dni):
    with pytest.raises(DatoInvalidoError):
        PersonaConcreta("Ana", dni)


def test_setter_dni_invalido_lanza_error():
    p = PersonaConcreta("Ana", "12345678")
    with pytest.raises(DatoInvalidoError):
        p.dni = "123"


def test_errores_de_persona_son_historial_error():
    with pytest.raises(HistorialError):
        PersonaConcreta("", "12345678")


# Medico

def test_medico_es_persona():
    m = Medico("Luis", "11111111", "12345", "Cardiología")
    assert isinstance(m, Persona)
    assert isinstance(m, Medico)


def test_medico_obtiene_datos():
    m = Medico("Luis", "11111111", "12345", "Cardiología")
    assert m.nombre == "Luis"
    assert m.dni == "11111111"
    assert m.matricula == "12345"
    assert m.especialidad == "Cardiología"


def test_medico_matricula_solo_digitos_en_constructor():
    with pytest.raises(DatoInvalidoError):
        Medico("Luis", "11111111", "ABC", "Cardiología")


def test_medico_setter_matricula_valida():
    m = Medico("Luis", "11111111", "12345", "Cardiología")
    m.matricula = "99999"
    assert m.matricula == "99999"


@pytest.mark.parametrize("matricula", ["", "12a45", "12 45", None])
def test_medico_setter_matricula_invalida(matricula):
    m = Medico("Luis", "11111111", "12345", "Cardiología")
    with pytest.raises(DatoInvalidoError):
        m.matricula = matricula


def test_medico_setter_especialidad_valida():
    m = Medico("Luis", "11111111", "12345", "Cardiología")
    m.especialidad = "Pediatría"
    assert m.especialidad == "Pediatría"


@pytest.mark.parametrize("especialidad", ["", "   ", None])
def test_medico_especialidad_invalida(especialidad):
    with pytest.raises(DatoInvalidoError):
        Medico("Luis", "11111111", "12345", especialidad)


def test_medico_descripcion_incluye_datos():
    m = Medico("Luis", "11111111", "12345", "Cardiología")
    desc = m.descripcion()
    assert isinstance(desc, str)
    assert "Luis" in desc
    assert "11111111" in desc
    assert "12345" in desc
    assert "Cardiología" in desc


# Paciente

def test_paciente_es_persona():
    p = Paciente("Marta", "22222222", "1990-05-17")
    assert isinstance(p, Persona)
    assert isinstance(p, Paciente)


def test_paciente_obtiene_fecha_nacimiento():
    p = Paciente("Marta", "22222222", "1990-05-17")
    assert p.fecha_nacimiento == "1990-05-17"


def test_paciente_setter_fecha_valida():
    p = Paciente("Marta", "22222222", "1990-05-17")
    p.fecha_nacimiento = "2000-01-31"
    assert p.fecha_nacimiento == "2000-01-31"


@pytest.mark.parametrize("fecha", ["17-05-1990", "1990/05/17", "1990-13-01", "1990-02-30", "", "hoy", None])
def test_paciente_fecha_invalida_lanza_error(fecha):
    with pytest.raises(DatoInvalidoError):
        Paciente("Marta", "22222222", fecha)


def test_paciente_setter_fecha_invalida_lanza_error():
    p = Paciente("Marta", "22222222", "1990-05-17")
    with pytest.raises(DatoInvalidoError):
        p.fecha_nacimiento = "no-es-fecha"


def test_paciente_descripcion_incluye_datos():
    p = Paciente("Marta", "22222222", "1990-05-17")
    desc = p.descripcion()
    assert isinstance(desc, str)
    assert "Marta" in desc
    assert "22222222" in desc
    assert "1990-05-17" in desc


def test_polimorfismo_descripcion_sobre_lista_de_personas():
    personas = [
        Medico("Luis", "11111111", "12345", "Cardiología"),
        Paciente("Marta", "22222222", "1990-05-17"),
    ]
    descripciones = [p.descripcion() for p in personas]
    assert all(isinstance(d, str) for d in descripciones)
    assert "Luis" in descripciones[0]
    assert "Marta" in descripciones[1]
