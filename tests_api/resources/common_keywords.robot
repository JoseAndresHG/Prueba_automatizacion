*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BASE_URL}    https://petstore.swagger.io/v2


*** Keywords ***
Añadir una mascota a la tienda
    [Arguments]    ${pet_id}    ${pet_name}    ${pet_status}=enable
    [Documentation]    Crea una mascota con la estructura exacta del Swagger
    ${category}=    Create Dictionary    id=0    name=string

    ${photos}=      Create List          string

    ${tag_1}=       Create Dictionary    id=3    name=string
    ${tags}=        Create List          ${tag_1}

    ${body}=    Create Dictionary
    ...    id=${pet_id}
    ...    category=${category}
    ...    name=${pet_name}
    ...    photoUrls=${photos}
    ...    tags=${tags}
    ...    status=${pet_status}

    ${response}=    POST   ${BASE_URL}/pet    json=${body}    expected_status=any

    Log    Respuesta del POST: ${response.content}
    RETURN    ${response}


Consultar Mascota Por ID
    [Arguments]    ${id}
    ${response}=    GET    ${BASE_URL}/pet/${id}    expected_status=any
    Log To Console    \nRespuesta completa: ${response.json()}
    RETURN    ${response}


Actualizar el nombre de la mascota y el estatus
    [Arguments]    ${pet_id}    ${nuevo_nombre}    ${nuevo_status}
    [Documentation]    Ejecuta un PUT para modificar una mascota existente

    ${category}=    Create Dictionary    id=0    name=string
    ${photos}=      Create List          string
    ${tag_1}=       Create Dictionary    id=0    name=string
    ${tags}=        Create List          ${tag_1}

    ${body}=    Create Dictionary
    ...    id=${pet_id}
    ...    category=${category}
    ...    name=${nuevo_nombre}
    ...    photoUrls=${photos}
    ...    tags=${tags}
    ...    status=${nuevo_status}

    ${response}=    PUT    ${BASE_URL}/pet    json=${body}    expected_status=any

    Log    Respuesta del PUT: ${response.content}
    RETURN    ${response}


Consultar Mascotas Por Estatus
    [Arguments]    ${estatus}
    [Documentation]
    ${parametros}=    Create Dictionary    status=${estatus}

    ${response}=    GET    ${BASE_URL}/pet/findByStatus    params=${parametros}    expected_status=any
    Log    Mascotas encontradas: ${response.content}
    RETURN    ${response}

Eliminar Mascota Por ID
    [Arguments]    ${id}
    [Documentation]    Elimina una mascota por su ID
    ${response}=    DELETE    ${BASE_URL}/pet/${id}    expected_status=any
    Log    Respuesta del DELETE: ${response.content}
    RETURN    ${response}
