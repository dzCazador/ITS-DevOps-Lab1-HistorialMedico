"""Tests del reporte PDF del sistema de historial médico."""

import pytest

from historial.excepciones import DatoInvalidoError, HistorialError, ReporteError
from historial.personas import Medico, Paciente
from historial.repositorio import RepositorioHistorial
from historial.reportes import generar_reporte_pdf


def _repo_con_datos():
    repo = RepositorioHistorial()
    repo.agregar_medico(Medico("José Gómez", "30111222", "1001", "clínica"))
    repo.agregar_paciente(Paciente("Ñandú Pérez", "40111222", "1990-05-10"))
    repo.registrar_atencion("40111222", "1001", "2026-01-15", "consulta")
    return repo


def test_genera_archivo_pdf_valido(tmp_path):
    ruta = tmp_path / "reporte.pdf"
    generar_reporte_pdf(_repo_con_datos(), str(ruta))
    assert ruta.read_bytes().startswith(b"%PDF")


def test_devuelve_la_ruta_escrita(tmp_path):
    ruta = str(tmp_path / "reporte.pdf")
    assert generar_reporte_pdf(_repo_con_datos(), ruta) == ruta


def test_repositorio_vacio_produce_pdf_valido(tmp_path):
    ruta = tmp_path / "vacio.pdf"
    generar_reporte_pdf(RepositorioHistorial(), str(ruta))
    assert ruta.read_bytes().startswith(b"%PDF")


def test_repositorio_none_lanza_dato_invalido(tmp_path):
    with pytest.raises(DatoInvalidoError):
        generar_reporte_pdf(None, str(tmp_path / "x.pdf"))


@pytest.mark.parametrize("ruta", ["", None, 123])
def test_ruta_invalida_lanza_dato_invalido(ruta):
    with pytest.raises(DatoInvalidoError):
        generar_reporte_pdf(RepositorioHistorial(), ruta)


def test_ruta_no_escribible_lanza_reporte_error(tmp_path):
    with pytest.raises(ReporteError) as info:
        generar_reporte_pdf(RepositorioHistorial(), str(tmp_path))
    assert isinstance(info.value, HistorialError)


def test_texto_con_acentos_se_acepta(tmp_path):
    ruta = tmp_path / "acentos.pdf"
    repo = RepositorioHistorial()
    repo.agregar_medico(Medico("María Núñez ñ á é í ó ú", "30111222", "2002", "pediatría"))
    generar_reporte_pdf(repo, str(ruta))
    assert ruta.read_bytes().startswith(b"%PDF")
