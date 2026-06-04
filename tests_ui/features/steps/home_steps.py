from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from utils.locators import RegistrationLocators


@step("el usuario navega a la página pagina {url}")
def step_impl(context, url):
    context.driver.get(url)


@step('el usuario selecciona el botón "{nombre_boton}"')
def step_seleccionar_boton_dinamico(context, nombre_boton):
    wait = WebDriverWait(context.driver, 5)
    try:
        xpath = getattr(RegistrationLocators, nombre_boton.upper())
    except AttributeError:
        raise AttributeError(
            f"ERROR: El botón '{nombre_boton}' no está definido en la clase RegistrationLocators."
        )
    boton = wait.until(
        ec.element_to_be_clickable((By.XPATH, xpath))
    )
    boton.click()


@step('el usuario inicia sesión con el usuario "{usuario}" y la contraseña "{contrasena}"')
def step_iniciar_sesion_completo(context, usuario, contrasena):
    wait = WebDriverWait(context.driver, 15)
    boton_nav_login = wait.until(
        ec.element_to_be_clickable((By.ID, "login2"))
    )
    boton_nav_login.click()

    input_usuario = wait.until(
        ec.visibility_of_element_located((By.ID, "loginusername"))
    )
    input_usuario.clear()
    input_usuario.send_keys(usuario)

    input_password = context.driver.find_element(By.ID, "loginpassword")
    input_password.clear()
    input_password.send_keys(contrasena)

    boton_submit = context.driver.find_element(By.XPATH, "//button[@onclick='logIn()']")
    boton_submit.click()


@step('el usuario ingresa "{texto}" en el campo "{nombre_variable}"')
def step_impl(context, texto, nombre_variable):
    xpath = getattr(RegistrationLocators, nombre_variable)

    elemento = WebDriverWait(context.driver, 5).until(
        ec.element_to_be_clickable((By.XPATH, xpath))
    )
    elemento.clear()
    elemento.send_keys(texto)


@then('el usuario debería ver su nombre de usuario en el menú')
def step_impl(context):
    wait = WebDriverWait(context.driver, 10)
    wait.until(ec.visibility_of_element_located((By.XPATH, "//a[contains(.,'Welcome JoseH')]")))
