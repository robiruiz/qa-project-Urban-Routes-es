# Urban Routes — Automatización de pruebas

## Descripción del proyecto

Proyecto del Sprint 9 del bootcamp **QA Engineer de TripleTen**.

El objetivo es automatizar las principales funcionalidades del proceso de solicitud de un taxi en la aplicación web **Urban Routes**, utilizando Python, Selenium WebDriver y Pytest.

El proyecto implementa el patrón de diseño **Page Object Model (POM)** para organizar los localizadores y métodos de interacción con la interfaz, facilitando el mantenimiento y la reutilización del código.

## Tecnologías utilizadas

- **Python:** lenguaje de programación utilizado para desarrollar las pruebas.
- **Selenium WebDriver:** automatización de interacciones con el navegador.
- **Pytest:** ejecución y validación de casos de prueba.
- **Google Chrome:** navegador utilizado para las pruebas.
- **PyCharm:** entorno de desarrollo.
- **Git y GitHub:** control de versiones y alojamiento del repositorio.

## Estructura del proyecto

```text
qa-project-Urban-Routes-es/
├── main.py
├── data.py
├── README.md
└── .gitignore
```

**main.py:** contiene la clase `UrbanRoutesPage`, que agrupa los localizadores y métodos de interacción, y la clase `TestUrbanRoutes`, que contiene las pruebas automatizadas.

**data.py:** almacena la URL del servidor de Urban Routes y los datos utilizados durante las pruebas.

**README.md:** documentación del proyecto, las tecnologías utilizadas y las instrucciones de ejecución.

**.gitignore:** excluye archivos locales, entornos virtuales, cachés y archivos temporales del repositorio.

## Pruebas automatizadas

Se implementaron nueve pruebas independientes que verifican las siguientes funcionalidades:

| Prueba | Funcionalidad |
|---|---|
| `test_set_route()` | Configurar las direcciones de origen y destino. |
| `test_select_comfort()` | Seleccionar la tarifa Comfort. |
| `test_add_phone()` | Introducir y confirmar un número telefónico mediante código SMS. |
| `test_add_card()` | Agregar una tarjeta de pago de prueba. |
| `test_message_driver()` | Introducir un mensaje para el conductor. |
| `test_blanket()` | Activar la opción de manta y pañuelos. |
| `test_ice_cream()` | Solicitar dos helados. |
| `test_search_taxi()` | Solicitar un taxi y verificar la aparición de la ventana de búsqueda. |
| `test_driver_info()` | Verificar el nombre, la calificación y la matrícula del vehículo del conductor asignado. |

Cada prueba utiliza las interacciones y validaciones correspondientes a su funcionalidad.

## Diseño de la automatización

La implementación utiliza el patrón Page Object Model (POM), que permite separar las interacciones con la interfaz de las validaciones de las pruebas.

El código se organiza principalmente en dos clases:

- `UrbanRoutesPage`: contiene los localizadores y métodos para interactuar con Urban Routes.
- `TestUrbanRoutes`: contiene los nueve métodos de prueba ejecutados por Pytest.

Se utilizan **esperas explícitas** mediante `WebDriverWait` y `expected_conditions` para sincronizar la automatización con los elementos y estados de la interfaz.

En la prueba de información del conductor, Selenium espera a que se complete la asignación antes de leer y validar sus datos.

## Requisitos previos

Para ejecutar el proyecto se necesita:

- Python instalado.
- Google Chrome instalado.
- Acceso a una instancia activa de Urban Routes proporcionada por TripleTen.
- Las bibliotecas Selenium y Pytest.

## Instalación y configuración

**1. Clonar el repositorio**

```bash
git clone https://github.com/robiruiz/qa-project-Urban-Routes-es.git
cd qa-project-Urban-Routes-es
```

**2. Crear un entorno virtual**

```bash
python -m venv .venv
```

**3. Activar el entorno virtual en Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**4. Instalar las dependencias**

```bash
python -m pip install selenium pytest
```

Selenium Manager permite gestionar ChromeDriver automáticamente en versiones recientes de Selenium, por lo que normalmente no es necesario descargarlo manualmente.

**5. Configurar el servidor**

Abrir el archivo `data.py` y actualizar `urban_routes_url` con la URL vigente de Urban Routes proporcionada por TripleTen.

Verificar que los datos de prueba correspondan al entorno utilizado.

## Ejecución de las pruebas

Desde la raíz del proyecto, con el entorno virtual configurado, ejecutar:

```bash
python -m pytest main.py::TestUrbanRoutes -v
```

Para ejecutar una sola prueba, por ejemplo la de información del conductor:

```bash
python -m pytest main.py::TestUrbanRoutes::test_driver_info -v
```

Para obtener información adicional durante la ejecución:

```bash
python -m pytest main.py::TestUrbanRoutes -v -rs --tb=short
```

## Resultado de las pruebas

La suite completa fue ejecutada localmente con Pytest, obteniendo el siguiente resultado:

**9 passed in 84.85s**

Las nueve pruebas automatizadas finalizaron correctamente, sin pruebas fallidas ni omitidas en esa ejecución.

Este resultado corresponde a una ejecución local del proyecto, utilizando una instancia activa de Urban Routes.

## Consideraciones

- La URL de Urban Routes puede cambiar al reiniciar o reemplazar el servidor de TripleTen.
- El funcionamiento de las pruebas depende de que la instancia de la aplicación esté disponible.
- Los datos de pago utilizados son ficticios y tienen fines de prueba.
- La solicitud del taxi incluye un mensaje válido para el conductor.
- La asignación del conductor puede requerir una espera adicional antes de mostrar su información.
- Las pruebas se ejecutan en Google Chrome mediante Selenium WebDriver.

## Autor

Proyecto desarrollado como parte del Sprint 9 del programa QA Engineer de TripleTen.

**Repositorio:** https://github.com/robiruiz/qa-project-Urban-Routes-es