*** Settings ***
Library    RequestsLibrary
Library    Collections
Resource        resources/common_keywords.robot


*** Test Cases ***
Añadir mascota a la tiensa
    Añadir una mascota a la tienda    4     Ramon

Consultar la mascota ingresada por ID
    Consultar Mascota Por ID    2
    
Actualizar mascota
    Actualizar el nombre de la mascota y el estatus     2     Luna     sold

Consultar mascota por status
    Consultar Mascotas Por Estatus     sold

Eliminar una mascota existente
   Eliminar Mascota Por ID    2

