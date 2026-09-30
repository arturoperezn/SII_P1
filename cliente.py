import requests

USER_URL = "http://127.0.0.1:5050"
FILE_URL = "http://127.0.0.1:5051"

def probar(nombre_prueba: str, respuesta, codigo_esperado: int):
    if respuesta.status_code == codigo_esperado:
        print(f"[OK] {nombre_prueba} (HTTP {respuesta.status_code})")
        return True
    else:
        print(f"[FAIL] {nombre_prueba} - Esperado: {codigo_esperado}, Obtenido: {respuesta.status_code}")
        print(f"       Respuesta: {respuesta.text}")
        return False

def run_tests():
    print("=== INICIANDO PRUEBAS AUTOMATIZADAS ===")

    # 1. Crear usuario Alicia
    r = requests.put(f"{USER_URL}/user", json={"name": "alicia", "password": "pwd"})
    if not probar("Crear usuario Alicia", r, 201):
        return
    data = r.json()
    uid_alicia = data["uid"]
    token_alicia = data["token"]
    
    headers_alicia = {"Authorization": f"Bearer {token_alicia}"}

    # 2. Subir documento privado
    r = requests.put(
        f"{FILE_URL}/file/{uid_alicia}/secret.txt",
        data="Contenido confidencial",
        headers={"Content-Type": "text/plain", **headers_alicia}
    )
    probar("Subir documento privado", r, 200)

    # 3. Leer documento privado SIN token (debe dar 401)
    r = requests.get(f"{FILE_URL}/file/{uid_alicia}/secret.txt")
    probar("Leer privado sin token (debe fallar 401)", r, 401)

    # 4. Leer documento privado CON token
    r = requests.get(f"{FILE_URL}/file/{uid_alicia}/secret.txt", headers=headers_alicia)
    probar("Leer privado con token del dueño", r, 200)

    # 5. Hacer público el documento
    r = requests.patch(
        f"{FILE_URL}/file/{uid_alicia}/secret.txt",
        json={"public": True},
        headers=headers_alicia
    )
    probar("Cambiar visibilidad a público", r, 200)

    # 6. Leer público SIN token (ahora debe dar 200)
    r = requests.get(f"{FILE_URL}/file/{uid_alicia}/secret.txt")
    probar("Leer documento público sin token", r, 200)

    # 7. Borrar documento
    r = requests.delete(f"{FILE_URL}/file/{uid_alicia}/secret.txt", headers=headers_alicia)
    probar("Borrar documento", r, 200)

if __name__ == "__main__":
    run_tests()