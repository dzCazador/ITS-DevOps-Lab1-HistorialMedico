# Sistema de Historial Médico

## Descripción general

Aplicación de consola en Python que permite registrar médicos, pacientes y atenciones médicas, consultar el historial de un paciente, calcular la facturación de un médico y exportar un reporte en PDF.

El proyecto está diseñado con programación orientada a objetos: clases abstractas para personas y atenciones, herencia, polimorfismo y encapsulamiento. Los datos se almacenan en memoria durante la ejecución; no hay persistencia en base de datos.

## Requisitos

- Python 3.10 o superior.
- Entorno virtual (`venv`) recomendado.
- Dependencias de `requirements.txt`: `fpdf2==2.9.0` y `pytest==9.2.0`.

## Instalación

Los comandos se ejecutan desde la carpeta raíz del repositorio `TP Final Entregar`.

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activarlo:

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

cmd:

```bat
.venv\Scripts\activate.bat
```

Instalar las dependencias (el archivo se encuentra en `historial_medico`):

```bash
pip install -r historial_medico\requirements.txt
```

## Ejecución

Desde la carpeta `historial_medico`:

```bash
python main.py
```

El menú de consola muestra las siguientes opciones:

| Opción | Acción |
|--------|--------|
| 1 | Registrar médico (nombre, DNI, matrícula, especialidad) |
| 2 | Registrar paciente (nombre, DNI, fecha de nacimiento) |
| 3 | Registrar atención (DNI del paciente, matrícula del médico, fecha, tipo) |
| 4 | Listar médicos |
| 5 | Listar pacientes |
| 6 | Ver historial de un paciente (por DNI) |
| 7 | Ver facturación de un médico (por matrícula) |
| 8 | Guardar reporte PDF |
| 0 | Salir |

Notas de uso:

- Las fechas deben tener el formato `YYYY-MM-DD`.
- El tipo de atención acepta `consulta`, `urgencia` o `control`.
- Una opción inválida vuelve a solicitar la selección.
- Los errores de validación o de negocio se muestran como `Error: <mensaje>` y el menú continúa.

## Pruebas

Desde la carpeta `historial_medico`:

```bash
pytest -v
```

La configuración está en `pytest.ini` (`testpaths = tests`, `pythonpath = .`). Las pruebas cubren:

| Archivo | Cobertura |
|---------|-----------|
| `tests/test_personas.py` | Clase abstracta `Persona`, `Medico` y `Paciente`, validaciones de DNI, matrícula, especialidad y fecha, encapsulamiento y polimorfismo de `descripcion()`. |
| `tests/test_atenciones.py` | Clase abstracta `Atencion`, subclases, costos, validación de fecha, polimorfismo sobre listas mixtas y función fábrica `crear_atencion`. |
| `tests/test_repositorio.py` | Alta y búsqueda de entidades, duplicados, historial por paciente, facturación por médico y copias de listas. |
| `tests/test_menu.py` | Opciones del menú, opción inválida, salida, manejo de errores y escritura del PDF con entrada inyectada. |
| `tests/test_reportes.py` | Generación de PDF válido, repositorio vacío, rutas inválidas, error de escritura y texto con acentos. |
| `tests/test_excepciones.py` | Jerarquía de excepciones. |
| `tests/test_estructura.py` | Existencia de la versión del paquete. |

## Estructura del proyecto

```text
TP Final Entregar/
├── .gitignore
└── historial_medico/
    ├── main.py                 # Punto de entrada
    ├── pytest.ini              # Configuración de pytest
    ├── requirements.txt        # Dependencias
    ├── historial/
    │   ├── __init__.py
    │   ├── atenciones.py       # Atencion y subclases, costos, crear_atencion
    │   ├── excepciones.py      # Jerarquía de excepciones
    │   ├── menu.py             # Menú de consola
    │   ├── personas.py         # Persona, Medico y Paciente
    │   ├── reportes.py         # Generación del PDF con fpdf2
    │   └── repositorio.py      # RepositorioHistorial (almacenamiento en memoria)
    └── tests/                  # Pruebas automatizadas
```

## Principios de POO

| Principio | Implementación | Archivo y clase |
|-----------|----------------|-----------------|
| Abstracción | `Persona` es una clase abstracta (`ABC`) con el método abstracto `descripcion()`. | `historial/personas.py`: `Persona` |
| Abstracción | `Atencion` es una clase abstracta con los métodos abstractos `tipo()` y `costo()`. | `historial/atenciones.py`: `Atencion` |
| Herencia | `Medico` y `Paciente` heredan de `Persona`. | `historial/personas.py`: `Medico`, `Paciente` |
| Herencia | `AtencionConsulta`, `Urgencia` y `Control` heredan de `Atencion`. | `historial/atenciones.py`: `AtencionConsulta`, `Urgencia`, `Control` |
| Polimorfismo | `descripcion()` se implementa en `Persona` (subclases `Medico` y `Paciente`). | `historial/personas.py`: `Medico.descripcion()`, `Paciente.descripcion()` |
| Polimorfismo | `tipo()` devuelve el nombre del tipo de atención en cada subclase. | `historial/atenciones.py`: `AtencionConsulta.tipo()`, `Urgencia.tipo()`, `Control.tipo()` |
| Polimorfismo | `costo()` devuelve el costo fijo de cada subclase; `Atencion.descripcion()` usa ambos métodos. | `historial/atenciones.py`: `costo()` en cada subclase, `Atencion.descripcion()` |
| Encapsulamiento | Atributos privados (`__nombre`, `__dni`, `__matricula`, etc.) expuestos mediante propiedades con getters y setters validados. | `historial/personas.py`: `Persona`, `Medico`, `Paciente` |
| Encapsulamiento | `paciente`, `medico` y `fecha` de `Atencion` son atributos privados con propiedades validadas. | `historial/atenciones.py`: `Atencion` |

## Manejo de errores

Todas las excepciones heredan de `HistorialError`, definida en `historial/excepciones.py`:

| Excepción | Uso |
|-----------|-----|
| `HistorialError` | Base del sistema. El menú la captura junto con `ValueError` y `TypeError`. |
| `DatoInvalidoError` | Valores inválidos: DNI, matrícula, nombre, especialidad, fechas, tipos de objeto y tipo de atención. Lanzada en `personas.py`, `atenciones.py`, `repositorio.py`, `reportes.py` y `menu.py`. |
| `EntidadDuplicadaError` | Alta de un médico con matrícula existente o de un paciente con DNI existente (`repositorio.py`). |
| `EntidadNoEncontradaError` | Búsqueda de médico por matrícula o paciente por DNI inexistente (`repositorio.py`). |
| `ReporteError` | Error al escribir el archivo PDF (`reportes.py`). |

## Reporte PDF

La opción 8 del menú solicita una ruta de archivo; si se deja vacía, usa `reporte.pdf` en el directorio de ejecución. El reporte incluye:

- Listado de médicos.
- Listado de pacientes.
- Listado de atenciones.
- Facturación total por médico.

El archivo generado no se versiona: la regla `*.pdf` del `.gitignore` lo excluye del repositorio.

## Costos de atención

Definidos como constantes en `historial/atenciones.py`:

| Tipo | Constante | Costo |
|------|-----------|-------|
| Consulta | `COSTO_CONSULTA` | 12000.0 |
| Urgencia | `COSTO_URGENCIA` | 18000.0 |
| Control | `COSTO_CONTROL` | 6000.0 |

## Control de versiones

### Ramas

| Rama | Uso |
|------|-----|
| `main` | Rama principal y estable. |
| `dev/cristian` | Rama de desarrollo sobre la que se trabaja y desde la que se integra a `main`. |

### Convención de commits

Se usa [Conventional Commits](https://www.conventionalcommits.org/) con el número de issue entre paréntesis al final del mensaje:

```text
feat(menu): agregar menú interactivo con manejo de errores try-except (#6)
```

### Seguimiento de issues

Las issues se gestionan en GitHub Projects con las columnas:

- Pendiente
- En curso
- Finalizada
