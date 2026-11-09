from historial.atenciones import COSTO_CONSULTA
from historial.menu import Menu
from historial.personas import Medico, Paciente
from historial.repositorio import RepositorioHistorial


class EntradaFalsa:
    """Simula input() con respuestas predefinidas."""

    def __init__(self, respuestas):
        self._respuestas = iter(respuestas)

    def __call__(self, prompt=""):
        return next(self._respuestas)


def _ejecutar(respuestas, repositorio=None):
    repo = repositorio if repositorio is not None else RepositorioHistorial()
    salida = []
    menu = Menu(repo, entrada=EntradaFalsa(respuestas), salida=salida.append)
    menu.ejecutar()
    return repo, "\n".join(salida)


def test_salir_con_0_termina_el_menu():
    _, texto = _ejecutar(["0"])
    assert "Saliendo" in texto


def test_opcion_invalida_vuelve_a_preguntar():
    _, texto = _ejecutar(["9", "abc", "0"])
    assert texto.count("Opción inválida") == 2
    assert "Saliendo" in texto


def test_registrar_medico_y_listarlo():
    respuestas = ["1", "Dr. House", "87654321", "12345", "Clinica", "4", "0"]
    repo, texto = _ejecutar(respuestas)
    medicos = repo.listar_medicos()
    assert len(medicos) == 1
    assert medicos[0].matricula == "12345"
    assert "Dr. House" in texto


def test_error_de_repositorio_se_muestra_y_el_menu_continua():
    respuestas = [
        "1", "Dr. House", "87654321", "12345", "Clinica",
        "1", "Dr. Otro", "11111111", "12345", "Clinica",
        "0",
    ]
    repo, texto = _ejecutar(respuestas)
    assert len(repo.listar_medicos()) == 1
    assert "ya existe un médico con matrícula 12345" in texto
    assert "Saliendo" in texto


def test_fecha_invalida_no_cierra_el_menu():
    respuestas = ["2", "Ana", "12345678", "1990-13-40", "0"]
    repo, texto = _ejecutar(respuestas)
    assert repo.listar_pacientes() == []
    assert "Error" in texto
    assert "Saliendo" in texto


def test_facturacion_muestra_total_del_medico():
    repo = RepositorioHistorial()
    repo.agregar_medico(Medico("Dr. House", "87654321", "12345", "Clinica"))
    repo.agregar_paciente(Paciente("Ana", "12345678", "1990-05-10"))
    repo.registrar_atencion("12345678", "12345", "2026-03-15", "consulta")
    _, texto = _ejecutar(["7", "12345", "0"], repositorio=repo)
    assert f"{COSTO_CONSULTA:.2f}" in texto


def test_opcion_pdf_escribe_en_la_ruta_indicada(tmp_path):
    ruta = tmp_path / "reporte.pdf"
    _, texto = _ejecutar(["8", str(ruta), "0"])
    assert ruta.exists()
    assert ruta.stat().st_size > 0
    assert "Saliendo" in texto
