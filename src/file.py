from quart import Quart, jsonify, request
from uuid import uuid4, uuid5, UUID
import os
from pathlib import Path

app = Quart(__name__)

files = {}  

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
    if token != str(uuid5(secret_uuid, uid)):
        return False
    return True

# Devuelve la lista de documentos de un usuario
@app.get('/file/<uid>')
async  def get_user_documents(uid):
    if not check_login(uid):
        return jsonify({"error": "Unauthorized"}), 401
    # El usuario está autenticado y tiene permiso, devuekve la lista de documentos
    user_documents = files.get(uid, {})
    return jsonify({"documents": user_documents}), 200

# Crea o actualiza documento de usuario
@app.put('/file/<uid>/<filename>')
async def create_or_update_user_document(uid, filename):
    if not check_login(uid):
        return jsonify({"error": "Unauthorized"}), 401
    # El usuario está autenticado y tiene permiso, crea o actualiza el documento
    user_documents = files.setdefault(uid, {})
    if filename not in user_documents:
        user_documents.append(filename)
    return jsonify({"message": f"Document '{filename}' created/updated for user '{uid}'."}), 200