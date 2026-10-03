import requests

USER_URL = "http://127.0.0.1:5050"
FILE_URL = "http://127.0.0.1:5051"

def run_tests():
    print("Iniciando pruebas de la API de usuario\n")

    # 1. Crear usuario Alicia
    r = requests.put(f"{USER_URL}/user", json={"name": "alicia", "password": "pwd"})
    if r.status_code == 201:
        print("[OK] Crear usuario Alicia (HTTP 201)")
        data = r.json()
        uid_alicia = data["uid"]
        token_alicia = data["token"]
    else:
        print(f"[FAIL] Crear usuario Alicia - Esperado: 201, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 2. Crear usuario Alicia que ya existe 
    r = requests.put(f"{USER_URL}/user", json={"name": "alicia", "password": "pwd2"})
    if r.status_code == 409:
        print("[OK] Crear usuario Alicia que ya existe (HTTP 409)")
    else:
        print(f"[FAIL] Crear usuario Alicia que ya existe - Esperado: 409, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 3. Crear usuario Alicia sin password 
    r = requests.put(f"{USER_URL}/user", json={"name": "alicia"})
    if r.status_code == 400:
        print("[OK] Crear usuario Alicia sin password (HTTP 400)")
    else:
        print(f"[FAIL] Crear usuario Alicia sin password - Esperado: 400, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 4. Crear usuario sin nombre 
    r = requests.put(f"{USER_URL}/user", json={"password": "pwd"})
    if r.status_code == 400:
        print("[OK] Crear usuario sin nombre (HTTP 400)")
    else:
        print(f"[FAIL] Crear usuario sin nombre - Esperado: 400, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 5. Crear usuario sin datos 
    r = requests.put(f"{USER_URL}/user", json={})
    if r.status_code == 400:
        print("[OK] Crear usuario sin datos (HTTP 400)")
    else:
        print(f"[FAIL] Crear usuario sin datos - Esperado: 400, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 6. Iniciar sesión con usuario Alicia
    r = requests.post(f"{USER_URL}/user", json={"name": "alicia", "password": "pwd"})
    if r.status_code == 200:
        print("[OK] Iniciar sesión con usuario Alicia (HTTP 200)")
        data = r.json()
        if data.get("token") == token_alicia:
            print("[OK] Token recibido coincide con el token esperado")
        else:
            print(f"[FAIL] Token recibido no coincide - Esperado: {token_alicia}, Obtenido: {data.get('token')}")
    else:
        print(f"[FAIL] Iniciar sesión con usuario Alicia - Esperado: 200, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    headers_alicia = {"Authorization": f"Bearer {token_alicia}"}

    # 7. Iniciar sesión con usuario Alicia con contraseña incorrecta (debe dar 401)
    r = requests.post(f"{USER_URL}/user", json={"name": "alicia", "password": "wrongpwd"})
    if r.status_code == 401:
        print("[OK] Iniciar sesión con usuario Alicia con contraseña incorrecta (HTTP 401)")
    else:
        print(f"[FAIL] Iniciar sesión con usuario Alicia con contraseña incorrecta - Esperado: 401, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 8. Iniciar sesión con usuario que no existe (debe dar 404)
    r = requests.post(f"{USER_URL}/user", json={"name": "sergio", "password": "pwd"})
    if r.status_code == 404:
        print("[OK] Iniciar sesión con usuario que no existe (HTTP 404)")
    else:
        print(f"[FAIL] Iniciar sesión con usuario que no existe - Esperado: 404, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 9. Iniciar sesión con usuario sin datos (debe dar 400)
    r = requests.post(f"{USER_URL}/user", json={})
    if r.status_code == 400:
        print("[OK] Iniciar sesión con usuario sin datos (HTTP 400)")
    else:
        print(f"[FAIL] Iniciar sesión con usuario sin datos - Esperado: 400, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 10. Iniciar sesión con usuario sin password (debe dar 400)
    r = requests.post(f"{USER_URL}/user", json={"name": "alicia"})
    if r.status_code == 400:
        print("[OK] Iniciar sesión con usuario sin password (HTTP 400)")
    else:
        print(f"[FAIL] Iniciar sesión con usuario sin password - Esperado: 400, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 11. Iniciar sesión con usuario sin nombre (debe dar 400)
    r = requests.post(f"{USER_URL}/user", json={"password": "pwd"})
    if r.status_code == 400:
        print("[OK] Iniciar sesión con usuario sin nombre (HTTP 400)")
    else:
        print(f"[FAIL] Iniciar sesión con usuario sin nombre - Esperado: 400, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 12. Cambiar contraseña de Alicia
    r = requests.patch(
        f"{USER_URL}/user",
        json={"password": "newpwd"},
        headers=headers_alicia
    )
    if r.status_code == 200:
        print("[OK] Cambiar contraseña de Alicia (HTTP 200)")
    else:
        print(f"[FAIL] Cambiar contraseña de Alicia - Esperado: 200, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 13. Iniciar sesión con usuario Alicia con la nueva contraseña
    r = requests.post(f"{USER_URL}/user", json={"name": "alicia", "password": "newpwd"})
    if r.status_code == 200:
        print("[OK] Iniciar sesión con usuario Alicia con la nueva contraseña (HTTP 200)")
    else:
        print(f"[FAIL] Iniciar sesión con usuario Alicia con la nueva contraseña - Esperado: 200, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 14. Iniciar sesión con usuario Alicia con la contraseña antigua (debe dar 401)
    r = requests.post(f"{USER_URL}/user", json={"name": "alicia", "password": "pwd"})
    if r.status_code == 401:
        print("[OK] Iniciar sesión con usuario Alicia con la contraseña antigua (HTTP 401)")
    else:
        print(f"[FAIL] Iniciar sesión con usuario Alicia con la contraseña antigua - Esperado: 401, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 15. Cambiar contraseña de Alicia sin estar logueada (sin token) (debe dar 401)
    r = requests.patch(
        f"{USER_URL}/user",
        json={"password": "anotherpwd"}
    )
    if r.status_code == 401:
        print("[OK] Cambiar contraseña de Alicia sin estar logueada (sin token) (HTTP 401)")
    else:
        print(f"[FAIL] Cambiar contraseña de Alicia sin estar logueada - Esperado: 401, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")
        return

    # 16. Cambiar contraseña de Alicia con token pero sin nueva contraseña (debe dar 400)
    r = requests.patch(
        f"{USER_URL}/user",
        json={},
        headers=headers_alicia
    )
    if r.status_code == 400:
        print("[OK] Cambiar contraseña de Alicia con token pero sin nueva contraseña (HTTP 400)")
    else:
        print(f"[FAIL] Cambiar contraseña de Alicia con token pero sin nueva contraseña - Esperado: 400, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    print("\nIniciando pruebas de la API de archivos\n")

    # Crear usuario Sergio para pruebas de archivos
    r = requests.put(f"{USER_URL}/user", json={"name": "sergio", "password": "pwd"})
    token_sergio = r.json()["token"]
    headers_sergio = {"Authorization": f"Bearer {token_sergio}"}

    # 17. Subir documento privado
    r = requests.put(
        f"{FILE_URL}/file/{uid_alicia}/secret.txt",
        data="Contenido confidencial",
        headers={"Content-Type": "text/plain", **headers_alicia}
    )
    if r.status_code == 201:
        print("[OK] Subir documento privado (HTTP 201)")
    else:
        print(f"[FAIL] Subir documento privado - Esperado: 201, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 18. Actualizar documento
    r = requests.put(
        f"{FILE_URL}/file/{uid_alicia}/secret.txt",
        data="Contenido actualizado",
        headers={"Content-Type": "text/plain", **headers_alicia}
    )
    if r.status_code == 200:
        print("[OK] Actualizar documento privado (HTTP 200)")
    else:
        print(f"[FAIL] Actualizar documento privado - Esperado: 200, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 19. Intentar crear o actualizar documento sin login (sin token)
    r = requests.put(
        f"{FILE_URL}/file/{uid_alicia}/secret.txt",
        data="Contenido sin login",
        headers={"Content-Type": "text/plain"}
    )
    if r.status_code == 401:
        print("[OK] Intentar crear o actualizar documento sin login (HTTP 401)")
    else:
        print(f"[FAIL] Intentar crear o actualizar documento sin login - Esperado: 401, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 20. Intentar crear o actualizar documento con token de otro usuario (Sergio)
    r = requests.put(
        f"{FILE_URL}/file/{uid_alicia}/secret.txt",
        data="Contenido con token de otro usuario",
        headers={"Content-Type": "text/plain", **headers_sergio}
    )
    if r.status_code == 401:
        print("[OK] Intentar crear o actualizar documento con token de otro usuario (HTTP 401)")    
    else:
        print(f"[FAIL] Intentar crear o actualizar documento con token de otro usuario - Esperado: 401, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 21. Intentar crear o actualizar documento sin contenido
    r = requests.put(
        f"{FILE_URL}/file/{uid_alicia}/secret.txt",
        data="",
        headers={"Content-Type": "text/plain", **headers_alicia}
    )
    if r.status_code == 400:
        print("[OK] Intentar crear o actualizar documento sin contenido (HTTP 400)")
    else:
        print(f"[FAIL] Intentar crear o actualizar documento sin contenido - Esperado: 400, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 22. Intentar crear o actualizar documento con nombre reservado 'metadata.json'
    r = requests.put(
        f"{FILE_URL}/file/{uid_alicia}/metadata.json",
        data="Contenido de metadata",
        headers={"Content-Type": "text/plain", **headers_alicia}
    )
    if r.status_code == 403:
        print("[OK] Intentar crear o actualizar documento con nombre reservado 'metadata.json' (HTTP 403)")
    else:
        print(f"[FAIL] Intentar crear o actualizar documento con nombre reservado 'metadata.json' - Esperado: 403, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 23. Obtener lista de documentos de Alicia con token
    r = requests.get(f"{FILE_URL}/file/{uid_alicia}", headers=headers_alicia)
    if r.status_code == 200:
        print("[OK] Obtener lista de documentos de Alicia con token (HTTP 200)")
        documents = r.json().get("documents", [])
        if "secret.txt" in documents:
            print("[OK] Documento 'secret.txt' está en la lista de documentos")
        else:
            print(f"[FAIL] Documento 'secret.txt' no está en la lista de documentos: {documents}")
    else:
        print(f"[FAIL] Obtener lista de documentos de Alicia con token - Esperado: 200, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 24. Obtener lista de documentos de Alicia sin token
    r = requests.get(f"{FILE_URL}/file/{uid_alicia}")
    if r.status_code == 401:
        print("[OK] Obtener lista de documentos de Alicia sin token (HTTP 401)")
    else:
        print(f"[FAIL] Obtener lista de documentos de Alicia sin token - Esperado: 401, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 25. Obtener lista de documentos de Alicia con token de otro usuario (Sergio)
    r = requests.get(f"{FILE_URL}/file/{uid_alicia}", headers=headers_sergio)
    if r.status_code == 401:
        print("[OK] Obtener lista de documentos de Alicia con token de otro usuario (HTTP 401)")
    else:
        print(f"[FAIL] Obtener lista de documentos de Alicia con token de otro usuario - Esperado: 401, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 26. Leer documento privado logueado con token del dueño
    r = requests.get(f"{FILE_URL}/file/{uid_alicia}/secret.txt", headers=headers_alicia)
    if r.status_code == 200:
        print("[OK] Leer documento privado logueado con token del dueño (HTTP 200)")
        if r.text == "Contenido actualizado":
            print("[OK] Contenido del documento coincide con lo esperado")
        else:
            print(f"[FAIL] Contenido del documento no coincide - Esperado: 'Contenido actualizado', Obtenido: '{r.text}'")
    else:
        print(f"[FAIL] Leer documento privado logueado con token del dueño - Esperado: 200, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 27. Leer documento privado SIN token 
    r = requests.get(f"{FILE_URL}/file/{uid_alicia}/secret.txt")
    if r.status_code == 401:
        print("[OK] Leer documento privado sin token (HTTP 401)")
    else:
        print(f"[FAIL] Leer documento privado sin token - Esperado: 401, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 28. Leer documento privado con token de otro usuario (Sergio)
    r = requests.get(f"{FILE_URL}/file/{uid_alicia}/secret.txt", headers=headers_sergio)
    if r.status_code == 401:
        print("[OK] Leer documento privado con token de otro usuario (HTTP 401)")
    else:
        print(f"[FAIL] Leer documento privado con token de otro usuario - Esperado: 401, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 29. Leer documento que no existe
    r = requests.get(f"{FILE_URL}/file/{uid_alicia}/nonexistent.txt", headers=headers_alicia)
    if r.status_code == 404:
        print("[OK] Leer documento que no existe (HTTP 404)")
    else:
        print(f"[FAIL] Leer documento que no existe - Esperado: 404, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 30. Leer documento reservado 'metadata.json'
    r = requests.get(f"{FILE_URL}/file/{uid_alicia}/metadata.json", headers=headers_alicia)
    if r.status_code == 403:
        print("[OK] Leer documento reservado 'metadata.json' (HTTP 403)")
    else:
        print(f"[FAIL] Leer documento reservado 'metadata.json' - Esperado: 403, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 31. Hacer público el documento
    r = requests.patch(
        f"{FILE_URL}/file/{uid_alicia}/secret.txt",
        json={"public": True},
        headers=headers_alicia
    )
    if r.status_code == 200:
        print("[OK] Hacer público el documento (HTTP 200)")
    else:
        print(f"[FAIL] Hacer público el documento - Esperado: 200, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 32. Modificar visibilidad de documento sin token 
    r = requests.patch(
        f"{FILE_URL}/file/{uid_alicia}/secret.txt",
        json={"public": False}
    )
    if r.status_code == 401:
        print("[OK] Modificar visibilidad de documento sin token (HTTP 401)")
    else:
        print(f"[FAIL] Modificar visibilidad de documento sin token - Esperado: 401, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 33. Modificar visibilidad de documento con token de otro usuario (Sergio)
    r = requests.patch(
        f"{FILE_URL}/file/{uid_alicia}/secret.txt",
        json={"public": False},
        headers=headers_sergio
    )
    if r.status_code == 401:
        print("[OK] Modificar visibilidad de documento con token de otro usuario (HTTP 401)")
    else:
        print(f"[FAIL] Modificar visibilidad de documento con token de otro usuario - Esperado: 401, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 34. Modificar visibilidad de documento reservado 'metadata.json'
    r = requests.patch(
        f"{FILE_URL}/file/{uid_alicia}/metadata.json",
        json={"public": False},
        headers=headers_alicia
    )
    if r.status_code == 403:
        print("[OK] Modificar visibilidad de documento reservado 'metadata.json' (HTTP 403)")
    else:
        print(f"[FAIL] Modificar visibilidad de documento reservado 'metadata.json' - Esperado: 403, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 35. Modificar visibilidad de documento que no existe
    r = requests.patch(
        f"{FILE_URL}/file/{uid_alicia}/nonexistent.txt",
        json={"public": False},
        headers=headers_alicia
    )
    if r.status_code == 404:
        print("[OK] Modificar visibilidad de documento que no existe (HTTP 404)")
    else:
        print(f"[FAIL] Modificar visibilidad de documento que no existe - Esperado: 404, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 36. Modificar visibilidad de documento sin parámetro 'public'
    r = requests.patch(
        f"{FILE_URL}/file/{uid_alicia}/secret.txt",
        json={},
        headers=headers_alicia
    )
    if r.status_code == 400:
        print("[OK] Modificar visibilidad de documento sin parámetro 'public' (HTTP 400)")
    else:
        print(f"[FAIL] Modificar visibilidad de documento sin parámetro 'public' - Esperado: 400, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 37. Leer documento público SIN token 
    r = requests.get(f"{FILE_URL}/file/{uid_alicia}/secret.txt")
    if r.status_code == 200:
        print("[OK] Leer documento público sin token (HTTP 200)")
        if r.text == "Contenido actualizado":
            print("[OK] Contenido del documento coincide con lo esperado")
        else:
            print(f"[FAIL] Contenido del documento no coincide - Esperado: 'Contenido actualizado', Obtenido: '{r.text}'")
    else:
        print(f"[FAIL] Leer documento público sin token - Esperado: 200, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 38. Leer documento público con token de otro usuario (Sergio)
    r = requests.get(f"{FILE_URL}/file/{uid_alicia}/secret.txt", headers=headers_sergio)
    if r.status_code == 200:
        print("[OK] Leer documento público con token de otro usuario (HTTP 200)")
        if r.text == "Contenido actualizado":
            print("[OK] Contenido del documento coincide con lo esperado")
        else:
            print(f"[FAIL] Contenido del documento no coincide - Esperado: 'Contenido actualizado', Obtenido: '{r.text}'")
    else:
        print(f"[FAIL] Leer documento público con token de otro usuario - Esperado: 200, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 39. Eliminar documento sin login (sin token)
    r = requests.delete(f"{FILE_URL}/file/{uid_alicia}/secret.txt")
    if r.status_code == 401:
        print("[OK] Eliminar documento sin login (sin token) (HTTP 401)")
    else:
        print(f"[FAIL] Eliminar documento sin login - Esperado: 401, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 40. Eliminar documento con token de otro usuario (Sergio)
    r = requests.delete(f"{FILE_URL}/file/{uid_alicia}/secret.txt", headers=headers_sergio)
    if r.status_code == 401:
        print("[OK] Eliminar documento con token de otro usuario (HTTP 401)")
    else:
        print(f"[FAIL] Eliminar documento con token de otro usuario - Esperado: 401, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 41. Eliminar documento que no existe
    r = requests.delete(f"{FILE_URL}/file/{uid_alicia}/nonexistent.txt", headers=headers_alicia)
    if r.status_code == 404:
        print("[OK] Eliminar documento que no existe (HTTP 404)")
    else:
        print(f"[FAIL] Eliminar documento que no existe - Esperado: 404, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 42. Eliminar documento reservado 'metadata.json'
    r = requests.delete(f"{FILE_URL}/file/{uid_alicia}/metadata.json", headers=headers_alicia)
    if r.status_code == 403:
        print("[OK] Eliminar documento reservado 'metadata.json' (HTTP 403)")
    else:
        print(f"[FAIL] Eliminar documento reservado 'metadata.json' - Esperado: 403, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

    # 43. Eliminar documento con token del dueño
    r = requests.delete(f"{FILE_URL}/file/{uid_alicia}/secret.txt", headers=headers_alicia)
    if r.status_code == 200:
        print("[OK] Eliminar documento con token del dueño (HTTP 200)")
    else:
        print(f"[FAIL] Eliminar documento con token del dueño - Esperado: 200, Obtenido: {r.status_code}")
        print(f"       Respuesta: {r.text}")

if __name__ == "__main__":
    run_tests()