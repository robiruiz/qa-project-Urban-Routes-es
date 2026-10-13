# Urban Routes - Pruebas automatizadas

## Descripción

Proyecto del Sprint 9 del bootcamp QA Engineer de TripleTen.

Se automatiza el proceso de solicitud de un taxi en la aplicación web Urban Routes mediante Selenium WebDriver y Pytest.

## Tecnologías utilizadas

- Python
- Selenium WebDriver
- Pytest
- Google Chrome
- PyCharm
- Git y GitHub

## Pruebas implementadas

La automatización comprueba:

1. Configuración de las direcciones de origen y destino.
2. Selección de la tarifa Comfort.
3. Introducción y confirmación del número telefónico.
4. Registro de una tarjeta de pago de prueba.
5. Introducción de un mensaje para el conductor.
6. Activación de manta y pañuelos.
7. Solicitud de dos helados.
8. Solicitud del taxi y aparición del modal de búsqueda.

## Organización del proyecto

- main.py: localizadores, métodos y pruebas automatizadas.
- data.py: URL de Urban Routes y datos de prueba.
- .gitignore: exclusiones de Git.
- README.md: documentación del proyecto.

## Instalación

Se requiere Python y Google Chrome.

Instalar las dependencias:

    python -m pip install selenium pytest

Selenium Manager puede gestionar ChromeDriver automáticamente.

## Ejecución de las pruebas

Actualizar la URL de Urban Routes en data.py con el servidor vigente proporcionado por TripleTen.

Desde la carpeta raíz del proyecto, ejecutar:

    python -m pytest main.py -v

## Observaciones

- La URL de pruebas puede cambiar o dejar de estar disponible.
- Los datos de pago utilizados son ficticios.
- Se utilizan esperas explícitas para sincronizar Selenium con la interfaz.