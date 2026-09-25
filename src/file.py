from quart import Quart, jsonify, request
from uuid import uuid4, uuid5, UUID
import os
from pathlib import Path
import json

app = Quart(__name__)

files_data_path = Path("/app/data")


# Carga o genera un UUID secreto para la aplicación, que se usará para generar tokens de usuario.
def _load_or_create_secret_uuid_env():
    secret_path = Path("app/shared_data/secret_uuid.txt")
    secret_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        secret_uuid = str(uuid4())
        with open(secret_path, "x") as f:
            f.write(secret_uuid)
        return secret_uuid
    except FileExistsError:
        with open(secret_path, "r") as f:
            secret_uuid = f.read().strip()
        return secret_uuid

secret_uuid = _load_or_create_secret_uuid_env()

# Comprueba si la petición actual trae un token válido de sesión
def check_login(uid):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "): 
        return False
    token = token.replace("Bearer ", "")
    if not token:
        return False
    if token != str(uuid5(UUID(secret_uuid), uid)):
        return False
    return True

# Devuelve la lista de documentos de un usuario con un UID dado, si el usuario está autenticado
@app.get('/file/<uid>')
async  def get_user_documents(uid: str):
    if not check_login(uid):
        return jsonify({"error": "No autorizado"}), 401
    # El usuario está autenticado y tiene permiso, devuekve la lista de documentos
    user_directory = files_data_path / uid
    if not user_directory.exists():
        return jsonify({"documents": []}), 200
    user_documents = []
    for f in user_directory.iterdir():
        if f.is_file():
            user_documents.append(f.name)
    return jsonify({"documents": user_documents}), 200

# Crea o actualiza documento de usuario
@app.put('/file/<uid>/<filename>')
async def create_or_update_user_document(uid, filename):
    if not check_login(uid):
        return jsonify({"error": "No autorizado"}), 401
    # El usuario está autenticado y tiene permiso, crea o actualiza el documento
    user_directory = files_data_path / uid
    user_directory.mkdir(parents=True, exist_ok=True)
    file_path = user_directory / filename
    data = await request.get_data()
    if not data:
        return jsonify({"error": "No se proporcionó contenido para el documento"}), 400
    with open(file_path, "wb") as f:
        f.write(data)
    return jsonify({"message": f"Document '{filename}' created/updated for user '{uid}'."}), 200

# Recupera documento de usuario
@app.get('/file/<uid>/<filename>')
async def get_user_document(uid, filename):
    if not check_login(uid):
        return jsonify({"error": "No autorizado"}), 401
    # El usuario está autenticado y tiene permiso, devuelve el documento
    file_path = files_data_path / uid / filename
    if not file_path.exists():
        return jsonify({"error": "Documento no encontrado"}), 404
    )
    return jsonify({"filename": filename, "content": data.decode('utf-8')}), 200