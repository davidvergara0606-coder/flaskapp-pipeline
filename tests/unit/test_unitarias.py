from werkzeug.security import check_password_hash


def test_registro_crea_usuario_con_clave_encriptada(
    client, buscar_usuario, datos_usuario
):
    datos = datos_usuario()
    respuesta = client.post("/auth/registro", json=datos)
    print(respuesta.status_code, respuesta.get_json())

    assert respuesta.status_code == 201
    assert respuesta.json == {"mensaje": "Usuario creado exitosamente"}
    guardado = buscar_usuario(datos["documento"])
    print(guardado)
    assert guardado["password"] != datos["password"]
    assert check_password_hash(guardado["password"], datos["password"]) is True


def test_registro_crear_usuario_sin_clave(client, buscar_usuario, datos_usuario):
    datos = datos_usuario()
    del datos["password"]

    respuesta = client.post("/auth/registro", json=datos)
    print(respuesta.status_code, respuesta.get_json())

    assert respuesta.status_code == 400
    buscar_usuario(datos["documento"])
    assert respuesta.json == {"mensaje": "No se ha digitado el password"}


def test_registro_con_clave_vacia(client, buscar_usuario, datos_usuario):
    datos = datos_usuario()
    datos["password"] = ""

    respuesta = client.post("/auth/registro", json=datos)
    print(respuesta.status_code, respuesta.get_json())

    assert respuesta.status_code == 400
    assert respuesta.json == {"mensaje": "No se ha digitado el password"}
    guardado = buscar_usuario(datos["documento"])
    assert guardado is None


def test_registro_clave_caracteres_minimos(client, buscar_usuario, datos_usuario):
    datos = datos_usuario()
    datos["password"] = "clave12"

    respuesta = client.post("/auth/registro", json=datos)
    print(respuesta.status_code, respuesta.get_json())

    assert respuesta.status_code == 400
    assert respuesta.json == {"mensaje": "password muy corta"}
    guardado = buscar_usuario(datos["documento"])
    assert guardado is None


def test_registro_clave_caracteres_maximos(client, buscar_usuario, datos_usuario):
    datos = datos_usuario()
    datos["password"] = (
        "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0w"
    )

    respuesta = client.post("/auth/registro", json=datos)
    print(respuesta.status_code, respuesta.get_json())

    assert respuesta.status_code == 400
    assert respuesta.json == {"mensaje": "password muy larga"}
    guardado = buscar_usuario(datos["documento"])
    assert guardado is None


def test_registro_con_documento_repetido(client, crear_usuario, datos_usuario):
    crear_usuario()
    datos = datos_usuario(correo="otro@zound.com")

    respuesta = client.post("/auth/registro", json=datos)
    print(respuesta.status_code, respuesta.get_json())

    assert respuesta.status_code == 400
    assert respuesta.json == {"mensaje": "El documento ya está registrado"}


def test_registro_clave_de_8_caracteres_es_aceptada(
    client, buscar_usuario, datos_usuario
):
    datos = datos_usuario()
    datos["password"] = "clave123"

    respuesta = client.post("/auth/registro", json=datos)
    print(respuesta.status_code, respuesta.get_json())

    assert respuesta.status_code == 201
    assert respuesta.json == {"mensaje": "Usuario creado exitosamente"}
    guardado = buscar_usuario(datos["documento"])
    assert guardado is not None


def test_login_correcto_devuelve_el_rol_como_texto(client, crear_usuario):
    datos = crear_usuario()

    respuesta = client.post(
        "/auth/login",
        json={"documento": datos["documento"], "password": datos["password"]},
    )
    print(respuesta.status_code, respuesta.get_json())

    assert respuesta.status_code == 200
    assert respuesta.json["mensaje"] == "Login exitoso"
    assert respuesta.json["id_rol"] == "1"


def test_login_con_clave_incorrecta(client, crear_usuario):
    datos = crear_usuario()

    respuesta = client.post(
        "/auth/login", json={"documento": datos["documento"], "password": "OtraClave99"}
    )
    print(respuesta.status_code, respuesta.get_json())

    assert respuesta.status_code == 401
    assert respuesta.json == {"mensaje": "Credenciales inválidas"}


def test_salida_mayor_al_stock_es_rechazada(client, crear_producto, stock_de):
    id_producto = crear_producto(stock_actual=5)

    respuesta = client.post(
        "/productos/salida", json={"id_producto": id_producto, "cantidad": 6}
    )
    print(respuesta.status_code, respuesta.get_json())

    assert respuesta.status_code == 400
    assert respuesta.json == {"mensaje": "Stock insuficiente para la salida"}
    assert stock_de(id_producto) == 5
