# 🏥 Sistema de Historial Médico

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)
![PDF](https://img.shields.io/badge/PDF-fpdf2-E34F26)
![License](https://img.shields.io/badge/licencia-educativa-lightgrey)

Mini sistema de consola en **Python** para que médicos registren pacientes y el historial de sus atenciones. Trabajo Práctico Integrador Final – Laboratorio I (ITS Cipolletti).

> [!IMPORTANT]
> Los datos viven **en memoria** (listas). Al cerrar la aplicación se pierden, como pide la consigna.

## 📑 Índice

- [Funcionalidades](#-funcionalidades)
- [Principios de POO aplicados](#-principios-de-poo-aplicados)
- [Estructura](#-estructura)
- [Requisitos](#️-requisitos)
- [Instalación y ejecución](#-instalación-y-ejecución)
- [Pruebas](#-pruebas)
- [Uso del menú](#️-uso-del-menú)
- [Tarifas](#-tarifas)
- [Control de versiones y gestión del proyecto](#-control-de-versiones-y-gestión-del-proyecto)
- [Licencia](#-licencia)

## ✨ Funcionalidades

- [x] Registrar médicos y pacientes (con validación de DNI, matrícula y fechas).
- [x] Registrar atenciones de tres tipos: consulta, urgencia y control.
- [x] Ver el historial clínico de un paciente, ordenado por fecha.
- [x] Calcular la facturación total de un médico.
- [x] Generar un reporte en PDF con médicos, pacientes y atenciones.

## 🧩 Principios de POO aplicados

| Principio | Dónde | Ejemplo |
|---|---|---|
| Abstracción | `personas.py`, `atenciones.py` | `Persona` y `Atencion` son clases abstractas (`ABC`) |
| Herencia | `personas.py`, `atenciones.py` | `Medico(Persona)`, `Urgencia(Atencion)` |
| Polimorfismo | `descripcion()`, `costo()`, `tipo()` | Cada tipo de atención calcula su costo distinto |
| Encapsulamiento | Todas las clases | Atributos `__privados` con `@property` (getter/setter) y validación |

## 📁 Estructura

<details>
<summary>Ver árbol de carpetas</summary>

```text
TP Final Entregar/
├── README.md
├── .gitignore
└── historial_medico/
    ├── main.py                  # Punto de entrada
    ├── historial/
    │   ├── excepciones.py       # Jerarquía de errores propios
    │   ├── personas.py          # Persona, Medico, Paciente
    │   ├── atenciones.py        # Atencion, AtencionConsulta, Urgencia, Control
    │   ├── repositorio.py       # Almacenamiento en listas (arrays) en memoria
    │   ├── reportes.py          # Generación del PDF con fpdf2
    │   └── menu.py              # Menú interactivo
    ├── tests/                   # Pruebas unitarias con pytest
    ├── requirements.txt
    └── pytest.ini
```

</details>

## ⚙️ Requisitos

- [x] Python 3.10 o superior
- [ ] Git (opcional, para control de versiones)

## 🚀 Instalación y ejecución

Desde la raíz del repositorio (`TP Final Entregar/`):

```powershell
# 1. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Instalar dependencias
cd historial_medico
pip install -r requirements.txt

# 3. Ejecutar la aplicación
python main.py
```

> [!TIP]
> Si PowerShell bloquea la activación, ejecutá una vez: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## 🧪 Pruebas

Desde `historial_medico/`, con el entorno virtual activado:

```powershell
pytest -v
```

## 🖥️ Uso del menú

```text
1. Registrar médico          5. Listar pacientes
2. Registrar paciente        6. Ver historial de un paciente
3. Registrar atención        7. Facturación total de un médico
4. Listar médicos            8. Generar reporte PDF
                             0. Salir
```

Fechas en formato `AAAA-MM-DD`. Tipos de atención: `consulta`, `urgencia`, `control`.

> [!NOTE]
> La opción 8 guarda `reporte.pdf` en la carpeta desde la que se ejecuta el programa. Los PDF están excluidos en `.gitignore`.

## 💰 Tarifas

| Tipo | Costo |
|---|---|
| Consulta | $12.000 |
| Urgencia | $18.000 |
| Control | $6.000 |

## 🔀 Control de versiones y gestión del proyecto

- Ramas: `main` (versión entregable) y `dev/cristian` (desarrollo).
- Commits en [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/), referenciando el issue con `(#N)`.
- Tablero: [GitHub Projects](https://github.com/users/dzCazador/projects/3) con columnas **Pendiente**, **En curso** y **Finalizada**.

> [!WARNING]
> No trabajar directamente en `main`. Todo el desarrollo ocurre en `dev/cristian` y se integra a `main` con `git merge --no-ff`.

## 📝 Licencia

Proyecto académico con fines educativos.
