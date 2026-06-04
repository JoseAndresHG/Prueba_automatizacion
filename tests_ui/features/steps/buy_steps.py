from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from utils.locators import RegistrationLocators, CartLocators
from selenium.common.exceptions import StaleElementReferenceException
from  utils.locators import CartLocators

@step('el usuario agrega el producto "{nombre_producto}" al carrito')
def step_agregar_producto_completo(context, nombre_producto):
    wait = WebDriverWait(context.driver, 15)

    xpath_producto = f"//a[contains(text(), '{nombre_producto}')]"
    boton_producto = wait.until(ec.element_to_be_clickable((By.XPATH, xpath_producto)))
    boton_producto.click()

    xpath_agregar_carrito = "//a[contains(text(), 'Add to cart')]"
    boton_agregar = wait.until(ec.element_to_be_clickable((By.XPATH, xpath_agregar_carrito)))
    boton_agregar.click()

    wait.until(ec.alert_is_present())
    alerta = context.driver.switch_to.alert
    alerta.accept()

    elemento = WebDriverWait(context.driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//a[contains(.,'Home (current)')]"))
    )
    elemento.click()


@when('el usuario agrega los siguientes productos al carrito')
def step_agregar_multiples_productos(context):
    for row in context.table:
        producto = row['PRODUCTO']

        context.execute_steps(f'''
            When el usuario agrega el producto "{producto}" al carrito
        ''')


@step('el carrito de compras debería mostrar los productos esperados')
def step_validar_productos_en_carrito(context):
    wait = WebDriverWait(context.driver, 15)
    boton_carrito = wait.until(
        ec.element_to_be_clickable((By.ID, "cartur"))
    )
    boton_carrito.click()

    wait.until(
        ec.presence_of_element_located((By.XPATH, "//tbody[@id='tbodyid']/tr"))
    )
    filas_productos = context.driver.find_elements(By.XPATH, "//tbody[@id='tbodyid']/tr")

    productos_en_pantalla = []
    for fila in filas_productos:
        columna_titulo = fila.find_element(By.XPATH, "./td[2]")
        productos_en_pantalla.append(columna_titulo.text.strip())

    if context.table:
        productos_esperados = [row['PRODUCTO'] for row in context.table]
    else:
        productos_esperados = [getattr(context, 'producto_actual', '')]

    for producto in productos_esperados:
        assert producto in productos_en_pantalla, \
            f" ERROR: El producto '{producto}' no se encontró en el carrito. Productos visibles: {productos_en_pantalla}"

    print(f" Validación exitosa. Todos los productos {productos_esperados} están en el carrito.")



@step('el usuario diligencia el formulario con los siguientes datos')
def step_impl(context):
    for row in context.table:
        for campo in row.headings:
            valor = row[campo]
            xpath = getattr(CartLocators, campo)

            elemento = WebDriverWait(context.driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, xpath))
            )

            elemento.clear()
            elemento.send_keys(valor)


@step('el usuario confirma la "{nombre_boton}" y valida el éxito de la compra')
def step_finalizar_y_validar_compra(context, nombre_boton):
    wait = WebDriverWait(context.driver, 15)

    try:
        xpath_boton_comprar = getattr(RegistrationLocators, nombre_boton.upper())
    except AttributeError:
        raise AttributeError(
            f"ERROR: El botón '{nombre_boton}' no existe en la clase RegistrationLocators."
        )
    boton_comprar = wait.until(ec.element_to_be_clickable((By.XPATH, xpath_boton_comprar)))
    boton_comprar.click()

    xpath_mensaje_exito = "//h2[contains(text(),'Thank you for your purchase!')]"

    mensaje_elemento = wait.until(
        ec.visibility_of_element_located((By.XPATH, xpath_mensaje_exito))
    )
    texto_esperado = "Thank you for your purchase!"
    texto_real = mensaje_elemento.text.strip()

    assert texto_esperado in texto_real, \
        f"ERROR: La validación falló. Se esperaba '{texto_esperado}' pero se encontró '{texto_real}'"

    boton_ok_modal = context.driver.find_element(By.XPATH, "//button[contains(text(),'OK')]")
    boton_ok_modal.click()

    print("¡Compra finalizada y validada exitosamente!")