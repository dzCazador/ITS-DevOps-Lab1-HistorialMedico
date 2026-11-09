"""Generación de reportes PDF del sistema de historial médico."""

from fpdf import FPDF

from historial.excepciones import DatoInvalidoError, ReporteError

_TITULO = "Reporte del sistema de Historial Médico"


def _latin1(texto):
    """Convierte a texto compatible con las fuentes core de PDF (latin-1)."""
    return str(texto).encode("latin-1", errors="replace").decode("latin-1")


def _seccion(pdf, titulo):
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, _latin1(titulo), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)


def _linea(pdf, texto):
    pdf.multi_cell(0, 6, _latin1(texto), new_x="LMARGIN", new_y="NEXT")


def generar_reporte_pdf(repositorio, ruta):
    """Escribe en `ruta` un PDF con médicos, pacientes, atenciones y facturación."""
    if repositorio is None:
        raise DatoInvalidoError("repositorio no puede ser None")
    if not isinstance(ruta, str) or not ruta.strip():
        raise DatoInvalidoError("ruta debe ser un texto no vacío")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, _latin1(_TITULO), new_x="LMARGIN", new_y="NEXT")

    _seccion(pdf, "Médicos")
    for m in repositorio.listar_medicos():
        _linea(pdf, f"{m.nombre} | DNI {m.dni} | Matrícula {m.matricula} | "
                    f"Especialidad {m.especialidad}")

    _seccion(pdf, "Pacientes")
    for p in repositorio.listar_pacientes():
        _linea(pdf, f"{p.nombre} | DNI {p.dni} | Nacimiento {p.fecha_nacimiento}")

    _seccion(pdf, "Atenciones")
    for a in repositorio.listar_atenciones():
        _linea(pdf, f"{a.fecha} | Paciente DNI {a.paciente.dni} | "
                    f"Médico matrícula {a.medico.matricula} | Tipo {a.tipo()} | "
                    f"Costo {a.costo():.2f}")

    _seccion(pdf, "Facturación por médico")
    for m in repositorio.listar_medicos():
        total = repositorio.facturacion_medico(m.matricula)
        _linea(pdf, f"{m.nombre} (matrícula {m.matricula}): total {total:.2f}")

    try:
        pdf.output(ruta)
    except OSError as exc:
        raise ReporteError(f"no se pudo escribir el reporte en {ruta!r}: {exc}") from exc
    return ruta
