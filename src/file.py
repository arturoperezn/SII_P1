from quart import Quart, jsonify, request
from uuid import uuid4, uuid5, UUID
import os
from pathlib import Path
import json

app = Quart(__name__)

files_data_path = Path("/app/data")


# Carga o genera un UUID secreto para la aplicación, que se usará para generar tokens de usuario.
def _load_or_create_secret_uuid_env():
    secret_path = Path("/app/shared_data/secret_uuid.txt")
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

# Función para escribir metadatos de usuario en un archivo JSON
def write_metadata(uid: str, metadata: dict):
    user_directory = files_data_path / uid
    user_directory.mkdir(parents=True, exist_ok=True)
    metadata_path = user_directory / "metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

# Función para leer metadatos de usuario desde un archivo JSON
def read_metadata(uid: str) -> dict:
    metadata_path = files_data_path / uid / "metadata.json"
    if not metadata_path.exists():
        return {}
    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

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
    data = await request.get_data()
    if not data:
        return jsonify({"error": "No se proporcionó contenido para el documento"}), 400
    user_directory = files_data_path / uid
    user_directory.mkdir(parents=True, exist_ok=True)
    file_path = user_directory / filename
    with open(file_path, "wb") as f:
        f.write(data)
    metadata = read_metadata(uid)
    if filename not in metadata:
        metadata[filename] = {"public" : False}
        write_metadata(uid, metadata)
    return jsonify({"message": f"Document '{filename}' created/updated for user '{uid}'."}), 200

# Recupera documento de usuario
@app.get('/file/<uid>/<filename>')
async def get_user_document(uid, filename):
    file_path = files_data_path / uid / filename
    if not file_path.exists() or filename == "metadata.json":
        return jsonify({"error": "Documento no encontrado"}), 404
    metadata = read_metadata(uid)
    is_public = metadata.get(filename, {}).get("public", False)
    if not is_public:
        if not check_login(uid):
            return jsonify({"error": "No autorizado para leer este documento privado"}), 401
    content = file_path.read_text(encoding="utf-8")
    return content, 200, {"Content-Type": "text/plain; charset=utf-8"}

# Elimina documento de usuario
@app.delete('/file/<uid>/<filename>')
async def delete_user_document(uid, filename):
    if not check_login(uid):
        return jsonify({"error": "No autorizado"}), 401
    # El usuario está autenticado y tiene permiso, elimina el documento
    file_path = files_data_path / uid / filename
    if not file_path.exists() or filename == "metadata.json":
        return jsonify({"error": "Documento no encontrado"}), 404
    file_path.unlink()
    metadata = read_metadata(uid)
    if filename in metadata:
        del metadata[filename]
        write_metadata(uid, metadata)
    return jsonify({"message": f"Document '{filename}' deleted for user '{uid}'."}), 200

# Modifica la visibilidad (pública) de un documento de usuario
@app.patch('/file/<uid>/<filename>')
async def modify_document_visibility(uid, filename):
    if not check_login(uid):
        return jsonify({"error": "No autorizado"}), 401
    # El usuario está autenticado y tiene permiso, modifica la visibilidad del documento
    file_path = files_data_path / uid / filename
    if not file_path.exists() or filename == "metadata.json":
        return jsonify({"error": "Documento no encontrado"}), 404
    data = await request.get_json()
    if not data or "public" not in data:
        return jsonify({"error": "Faltan parámetros requeridos"}), 400
    metadata = read_metadata(uid)
    if filename not in metadata:
        metadata[filename] = {}
    public = data.get("public")
    metadata[filename]["public"] = bool(public)
    write_metadata(uid, metadata)
    return jsonify({"message": f"Document '{filename}' visibility updated for user '{uid}' to {public}."}), 200