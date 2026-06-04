Feature: Agregar productos y realizar compra exitosa

  Scenario: Agregar múltiples productos y completar la compra con éxito
    Given el usuario navega a la página pagina https://www.demoblaze.com/
    When el usuario inicia sesión con el usuario "JoseH" y la contraseña "Test1234*"
    Then el usuario debería ver su nombre de usuario en el menú
    When el usuario agrega los siguientes productos al carrito
      | PRODUCTO |
      | Nexus 6 |
      | Samsung galaxy s6 |
    Then el carrito de compras debería mostrar los productos esperados
      | PRODUCTO |
      | Nexus 6 |
      | Samsung galaxy s6 |
      And el usuario selecciona el botón "REALIZAR_PEDIDO"
      And el usuario diligencia el formulario con los siguientes datos
        | NAME | COUNTRY | CITY | CREDIT_CARD | MONTH | YEAR |
        | Jose | Colombia | Bogota | 10992422220 | OCT | 2028 |
      Then el usuario confirma la "COMPRAR" y valida el éxito de la compra










