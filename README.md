Urban Routes — Pruebas automatizadas

Descripción

Proyecto del Sprint 9 del bootcamp QA Engineer de TripleTen.

El objetivo es automatizar las principales funcionalidades del proceso de solicitud de un taxi en la aplicación web Urban Routes, utilizando Selenium WebDriver, Python y Pytest.

El proyecto utiliza el patrón Page Object Model (POM) para separar las interacciones con la interfaz de usuario de las pruebas automatizadas.

Tecnologías utilizadas

Python

Selenium WebDriver

Pytest

Google Chrome

Selenium Manager

PyCharm

Git y GitHub

Arquitectura del proyecto

El archivo main.py contiene dos clases principales:

UrbanRoutesPage (Page Object)

Centraliza los localizadores y los métodos utilizados para interactuar con Urban Routes, como configurar direcciones, seleccionar tarifas, confirmar el teléfono y solicitar un taxi.

TestUrbanRoutes (pruebas automatizadas)

Contiene pruebas independientes que utilizan los métodos del Page Object.

Cada prueba sigue tres etapas:

Precondiciones: preparar el estado necesario de la aplicación.

Acción: ejecutar la funcionalidad correspondiente.

Validación: comprobar el resultado esperado mediante aserciones.

Se utilizan los métodos setup_method() y teardown_method() para crear y cerrar una sesión independiente de Chrome para cada prueba.

Escenarios de prueba

Test

Funcionalidad

Estado

test_set_route()

Configurar direcciones de origen y destino

Implementado

test_select_comfort()

Seleccionar tarifa Comfort

Implementado

test_add_phone()

Agregar y confirmar teléfono mediante SMS

Implementado

test_add_card()

Agregar tarjeta de pago de prueba

Implementado

test_message_driver()

Escribir un mensaje para el conductor

Implementado

test_blanket()

Activar manta y pañuelos

Implementado

test_ice_cream()

Solicitar dos helados

Implementado

test_search_taxi()

Solicitar un taxi y verificar el modal de búsqueda

Implementado

test_driver_info()

Verificar la información del conductor asignado

Pendiente

Las primeras ocho pruebas se ejecutaron individualmente y también como conjunto.

Última ejecución conjunta registrada:

8 passed in 63.14s

La novena prueba está pendiente de implementación y validación debido a un problema del servicio de pedidos de Urban Routes.

Organización del proyecto

main.py: clases Page Object y pruebas automatizadas.

data.py: URL del servidor y datos de prueba.

.gitignore: exclusiones de archivos locales y temporales.

README.md: documentación del proyecto.

Requisitos e instalación

Se necesita:

Python.

Google Chrome.

Acceso a una instancia vigente de Urban Routes.

Instalar las dependencias desde la carpeta raíz del proyecto:

python -m pip install selenium pytest

Selenium Manager permite gestionar ChromeDriver automáticamente en instalaciones compatibles.

Configuración

Antes de ejecutar las pruebas, actualizar el valor urban_routes_url en data.py con la URL vigente proporcionada por TripleTen.

Verificar también que los datos de prueba correspondan al entorno utilizado.

Ejecución

Para ejecutar todas las pruebas implementadas:

python -m pytest main.py -v

Para ejecutar un test individual:

python -m pytest main.py::TestUrbanRoutes::test_add_phone -s -q --tb=short

Para comprobar la sintaxis:

python -m py_compile main.py data.py

Cada prueba debe ejecutarse de manera independiente, sin depender de los resultados de otras pruebas.

Sincronización con la interfaz

Se utilizan principalmente esperas explícitas mediante WebDriverWait y las condiciones de Selenium para esperar elementos visibles o interactivos.

Incidencia conocida: creación de pedidos

Durante las pruebas se detectó un problema en la creación de pedidos de Urban Routes.

Al solicitar un taxi, la petición order puede devolver HTTP 500 con la respuesta:

{"status":500,"error":"UnexpectedError"}

El problema se reprodujo manualmente desde Chrome, sin utilizar Selenium, y persistió al cambiar de instancia del servidor.

La incidencia fue reportada a TripleTen y se encuentra pendiente de respuesta.

Esta situación impide comprobar de manera confiable la asignación del conductor y completar el escenario test_driver_info().

El éxito de test_search_taxi() únicamente confirma la aparición del modal de búsqueda; no garantiza que el servidor haya completado la asignación de un conductor.

Observaciones

Las instancias de Urban Routes pueden cambiar o dejar de estar disponibles.

Los datos de tarjeta utilizados en las pruebas son ficticios.

Los tests deben ser independientes y contar con validaciones propias.

La aprobación final del proyecto depende de completar y verificar los nueve escenarios requeridos.