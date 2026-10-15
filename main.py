import data
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    comfort_tariff = (
        By.XPATH,
        "//div[contains(concat(' ',normalize-space(@class),' '),' tcard ')][.//div[contains(@class,'tcard-title') and normalize-space()='Comfort']]"
    )

    order_taxi_button = (
        By.CSS_SELECTOR,
        ".results-text button.button.round"
    )

    # Campo para introducir el número telefónico
    phone_field = (By.ID, "phone")

    # Botón Siguiente del formulario telefónico
    phone_next_button = (
        By.CSS_SELECTOR,
        ".number-picker .section.active button[type='submit']"
    )

    # Elemento que abre el formulario del teléfono
    phone_open_button = (
        By.CSS_SELECTOR,
        ".form .np-button"
    )

    # Campo para introducir el código de confirmación SMS
    sms_code_field = (
        By.CSS_SELECTOR,
        ".number-picker .section.active input#code"
    )

    # Botón Confirmar del formulario SMS
    sms_confirm_button = (
        By.XPATH,
        "//div[contains(@class,'number-picker')]//button[@type='submit' and normalize-space()='Confirmar']"
    )

    # Opción para agregar una tarjeta desde Método de pago
    add_card_button = (
        By.CSS_SELECTOR,
        ".payment-picker .pp-row.disabled"
    )

    # Campo donde se introduce el número de tarjeta
    card_number_field = (By.ID, "number")

    # Campo del código CVV de la tarjeta
    card_cvv_field = (
        By.CSS_SELECTOR,
        ".card-code-input input#code.card-input"
    )

    # Botón para agregar la tarjeta
    add_card_submit_button = (
        By.CSS_SELECTOR,
        ".payment-picker .pp-buttons button[type='submit']"
    )

    # Ventana de selección del método de pago
    payment_modal = (
        By.CSS_SELECTOR,
        ".payment-picker.open .section.active"
    )

    # Control que abre la ventana Método de pago
    payment_method_button = (
        By.CSS_SELECTOR,
        ".tariff-picker .form .pp-button.filled"
    )

    # Texto del método de pago seleccionado
    selected_payment_method = (
        By.CSS_SELECTOR,
        ".tariff-picker .form .pp-button.filled .pp-value-text"
    )

    # Botón para cerrar la ventana Método de pago
    payment_modal_close_button = (
        By.CSS_SELECTOR,
        ".payment-picker.open .section.active .section-close"
    )

    # Campo Mensaje para el conductor
    driver_message_field = (By.ID, "comment")

    # Interruptor para solicitar manta y pañuelos
    blanket_and_tissues_checkbox = (
        By.XPATH,
        "//div[contains(@class, 'r-type-switch')][.//div[normalize-space()='Manta y pañuelos']]//input[@type='checkbox']"
    )

    # Botón + del contador de helados
    ice_cream_plus_button = (
        By.XPATH,
        "//div[contains(@class, 'r-counter-container')][.//div[contains(@class, 'r-counter-label') and normalize-space()='Helado']]//div[contains(@class, 'counter-plus')]"
    )

    # Cantidad seleccionada de helados
    ice_cream_counter = (
        By.XPATH,
        "//div[contains(@class, 'r-counter-container')][.//div[contains(@class, 'r-counter-label') and normalize-space()='Helado']]//div[contains(@class, 'counter-value')]"
    )

    # Botón final para solicitar el taxi
    final_order_taxi_button = (
        By.CSS_SELECTOR,
        ".smart-button-wrapper button.smart-button"
    )

    # Título del modal de búsqueda del automóvil
    taxi_search_modal = (
        By.XPATH,
        "//div[contains(@class, 'order') and contains(@class, 'shown')]"
        "//div[contains(@class, 'order-header-title') "
        "and normalize-space()='Buscar automóvil']"
    )

    # Número telefónico mostrado después de confirmar el SMS
    confirmed_phone_text = (
        By.CSS_SELECTOR,
        ".tariff-picker .form .np-button.filled .np-text"
    )

    # Información del conductor asignado
    driver_name = (
        By.CSS_SELECTOR,
        ".order-buttons > .order-btn-group:first-child > div:nth-child(2)"
    )

    driver_rating = (
        By.CSS_SELECTOR,
        ".order-btn-rating"
    )

    driver_car_number = (
        By.CSS_SELECTOR,
        ".order-number .number"
    )

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        from_input = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.from_field
            )
        )
        from_input.send_keys(from_address)

    def set_to(self, to_address):
        to_input = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.to_field
            )
        )
        to_input.send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def open_taxi_order_form(self):
        taxi_button = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(
                self.order_taxi_button
            )
        )
        taxi_button.click()

    def select_comfort_tariff(self):
        comfort_card = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(
                self.comfort_tariff
            )
        )
        comfort_card.click()

    def check_comfort_tariff_selected(self):
        comfort_card = self.driver.find_element(
            *self.comfort_tariff
        )

        classes = comfort_card.get_attribute("class").split()

        assert "active" in classes, (
            "La tarifa Comfort no quedó seleccionada"
        )

    def set_phone_number(self, phone_number):
        phone_input = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.phone_field
            )
        )

        phone_input.clear()
        phone_input.send_keys(phone_number)

    def click_phone_next_button(self):
        next_button = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(
                self.phone_next_button
            )
        )
        next_button.click()

    def open_phone_modal(self):
        phone_button = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(
                self.phone_open_button
            )
        )
        phone_button.click()

    def set_sms_code(self, code):
        sms_input = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.sms_code_field
            )
        )
        sms_input.clear()
        sms_input.send_keys(code)

    def click_sms_confirm_button(self):
        confirm_button = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(
                self.sms_confirm_button
            )
        )
        confirm_button.click()

    def confirm_phone_number(self, phone_number):
        # Abrir el formulario telefónico
        self.open_phone_modal()

        # Introducir el número
        self.set_phone_number(phone_number)

        # Solicitar el código SMS
        self.click_phone_next_button()

        # Esperar a que aparezca el campo SMS
        WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.sms_code_field
            )
        )

        # Recuperar el código de confirmación
        sms_code = retrieve_phone_code(self.driver)

        # Introducir el código SMS
        self.set_sms_code(sms_code)

        # Confirmar el número telefónico
        self.click_sms_confirm_button()

        # Comprobar que desaparezca el formulario SMS
        WebDriverWait(self.driver, 15).until(
            expected_conditions.invisibility_of_element_located(
                self.sms_code_field
            )
        )

    def get_phone_number(self):
        phone_element = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.confirmed_phone_text
            )
        )

        return phone_element.text

    def open_payment_method(self):
        payment_button = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(
                self.payment_method_button
            )
        )
        payment_button.click()

        WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.payment_modal
            )
        )

    def open_add_card_form(self):
        add_card_option = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(
                self.add_card_button
            )
        )
        add_card_option.click()

        WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.card_number_field
            )
        )

    def set_card_number(self, card_number):
        card_input = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.card_number_field
            )
        )
        card_input.clear()
        card_input.send_keys(card_number)

    def set_card_cvv(self, card_cvv):
        cvv_input = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.card_cvv_field
            )
        )
        cvv_input.clear()
        cvv_input.send_keys(card_cvv)

        # El CVV debe perder el enfoque para habilitar Agregar
        cvv_input.send_keys(Keys.TAB)

    def submit_card(self):
        submit_button = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(
                self.add_card_submit_button
            )
        )
        submit_button.click()

        WebDriverWait(self.driver, 15).until(
            expected_conditions.invisibility_of_element_located(
                self.card_number_field
            )
        )

    def add_card(self, card_number, card_cvv):
        self.open_payment_method()
        self.open_add_card_form()
        self.set_card_number(card_number)
        self.set_card_cvv(card_cvv)
        self.submit_card()

    def get_selected_payment_method(self):
        payment_text = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.selected_payment_method
            )
        )
        return payment_text.text

    def close_payment_modal(self):
        close_button = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(
                self.payment_modal_close_button
            )
        )
        close_button.click()


    def set_message_for_driver(self, message):
        message_input = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.driver_message_field
            )
        )
        message_input.clear()
        message_input.send_keys(message)

    def get_message_for_driver(self):
        message_input = self.driver.find_element(
            *self.driver_message_field
        )
        return message_input.get_property("value")


    def enable_blanket_and_tissues(self):
        checkbox = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                self.blanket_and_tissues_checkbox
            )
        )

        if not checkbox.is_selected():
            switch_container = checkbox.find_element(
                By.XPATH,
                "./parent::div"
            )
            switch_container.click()

    def is_blanket_and_tissues_selected(self):
        checkbox = self.driver.find_element(
            *self.blanket_and_tissues_checkbox
        )
        return checkbox.is_selected()

    def add_two_ice_creams(self):
        plus_button = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(
                self.ice_cream_plus_button
            )
        )
        plus_button.click()
        plus_button.click()

    def request_taxi(self):
        taxi_button = WebDriverWait(self.driver, 15).until(
            expected_conditions.element_to_be_clickable(
                self.final_order_taxi_button
            )
        )
        taxi_button.click()

    def get_ice_cream_count(self):
        counter = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.ice_cream_counter
            )
        )
        return int(counter.text)

    def wait_for_taxi_search_modal(self):
        return WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.taxi_search_modal
            )
        )

    def get_driver_info(self):
        # Esperar a que se asigne un conductor real
        WebDriverWait(self.driver, 60).until(
            expected_conditions.visibility_of_element_located(
                self.driver_rating
            )
        )

        # Esperar a que aparezca el nombre del conductor
        name = WebDriverWait(self.driver, 30).until(
            expected_conditions.visibility_of_element_located(
                self.driver_name
            )
        ).text.strip()

        # Esperar a que aparezca la calificación
        rating = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.driver_rating
            )
        ).text.strip()

        # Esperar a que aparezca la matrícula
        car_number = WebDriverWait(self.driver, 15).until(
            expected_conditions.visibility_of_element_located(
                self.driver_car_number
            )
        ).text.strip()

        return {
            "name": name,
            "rating": rating,
            "car_number": car_number
        }


class TestUrbanRoutes:
    def setup_method(self):
        # Habilitar los registros de rendimiento de Chrome
        options = webdriver.ChromeOptions()
        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"}
        )

        # Crear un navegador nuevo para cada test
        self.driver = webdriver.Chrome(options=options)

    def test_set_route(self):
        # Precondición: abrir Urban Routes
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Acción: configurar origen y destino
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Validación: comprobar ambas direcciones
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort(self):
        # Precondiciones: abrir Urban Routes y configurar direcciones
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        routes_page.open_taxi_order_form()

        # Acción: seleccionar la tarifa Comfort
        routes_page.select_comfort_tariff()

        # Validación: comprobar que Comfort quedó seleccionada
        routes_page.check_comfort_tariff_selected()

    def test_add_phone(self):
        # Precondiciones: abrir Urban Routes
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Configurar las direcciones
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Abrir el formulario y seleccionar Comfort
        routes_page.open_taxi_order_form()
        routes_page.select_comfort_tariff()

        # Acción: introducir y confirmar el teléfono
        routes_page.confirm_phone_number(data.phone_number)

        # Validación: comprobar que quedó registrado
        assert (
                routes_page.get_phone_number().lstrip("+")
                == data.phone_number.lstrip("+")
        ), "El número telefónico confirmado no coincide"

    def test_add_card(self):
        # Precondiciones: abrir Urban Routes
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Configurar origen y destino
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Abrir el formulario y seleccionar Comfort
        routes_page.open_taxi_order_form()
        routes_page.select_comfort_tariff()

        # Confirmar el número telefónico
        routes_page.confirm_phone_number(data.phone_number)

        # Acción: agregar una tarjeta
        routes_page.add_card(
            data.card_number,
            data.card_code
        )

        # Cerrar el modal de método de pago
        routes_page.close_payment_modal()

        # Validación: comprobar el método seleccionado
        assert routes_page.get_selected_payment_method() == "Tarjeta", (
            "La tarjeta no quedó seleccionada como método de pago"
        )

    def test_message_driver(self):
        # Precondiciones: abrir Urban Routes
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Configurar direcciones
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Seleccionar Comfort
        routes_page.open_taxi_order_form()
        routes_page.select_comfort_tariff()

        # Acción: escribir el mensaje al conductor
        routes_page.set_message_for_driver(
            data.message_for_driver
        )

        # Validación: comprobar el mensaje escrito
        assert (
                routes_page.get_message_for_driver()
                == data.message_for_driver
        ), "El mensaje para el conductor no coincide"

    def test_blanket(self):
        # Precondiciones: abrir Urban Routes
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Configurar las direcciones
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Abrir las opciones del taxi y seleccionar Comfort
        routes_page.open_taxi_order_form()
        routes_page.select_comfort_tariff()

        # Acción: activar manta y pañuelos
        routes_page.enable_blanket_and_tissues()

        # Validación: comprobar que quedó activada
        assert routes_page.is_blanket_and_tissues_selected(), (
            "La opción Manta y pañuelos no quedó activada"
        )

    def test_ice_cream(self):
        # Precondiciones: abrir Urban Routes
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Configurar las direcciones
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Abrir el formulario y seleccionar Comfort
        routes_page.open_taxi_order_form()
        routes_page.select_comfort_tariff()

        # Acción: pedir dos helados
        routes_page.add_two_ice_creams()

        # Validación: comprobar la cantidad
        assert routes_page.get_ice_cream_count() == 2, (
            "La cantidad de helados no es 2"
        )

    def test_search_taxi(self):
        # Precondiciones: abrir Urban Routes
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Configurar las direcciones
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Abrir el formulario y seleccionar Comfort
        routes_page.open_taxi_order_form()

        routes_page.select_comfort_tariff()

        # Confirmar teléfono para habilitar el pedido
        routes_page.confirm_phone_number(data.phone_number)

        # Agregar un mensaje válido para el conductor
        routes_page.set_message_for_driver(data.message_for_driver)

        # Validar que el mensaje quedó registrado
        assert (
                routes_page.get_message_for_driver()
                == data.message_for_driver
        ), "El mensaje para el conductor no coincide"

        # Acción: solicitar un taxi
        routes_page.request_taxi()

        # Validación: comprobar el modal de búsqueda
        search_modal = routes_page.wait_for_taxi_search_modal()

        assert search_modal.is_displayed(), (
            "No apareció el modal de búsqueda del taxi"
        )

    def test_driver_info(self):
        # Precondiciones: abrir Urban Routes
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Configurar origen y destino
        routes_page.set_route(
            data.address_from,
            data.address_to
        )

        # Abrir el formulario y seleccionar Comfort
        routes_page.open_taxi_order_form()
        routes_page.select_comfort_tariff()

        # Confirmar el número telefónico
        routes_page.confirm_phone_number(data.phone_number)

        # Agregar mensaje válido para el conductor
        routes_page.set_message_for_driver(data.message_for_driver)

        # Verificar que el mensaje se escribió correctamente
        assert (
                routes_page.get_message_for_driver()
                == data.message_for_driver
        ), "El mensaje para el conductor no coincide"

        # Solicitar un taxi
        routes_page.request_taxi()

        # Esperar y obtener la información del conductor
        driver_info = routes_page.get_driver_info()

        # Comprobar el nombre
        assert driver_info["name"], "No aparece el nombre del conductor"

        # Comprobar la calificación
        rating = float(driver_info["rating"].replace(",", "."))
        assert 0 < rating <= 5, "La calificación del conductor no es válida"

        # Comprobar la matrícula
        assert driver_info["car_number"], "No aparece la matrícula del automóvil"

    def teardown_method(self):
        self.driver.quit()

