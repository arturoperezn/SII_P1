from quart import Quart, jsonify, request
from uuid import uuid4, uuid5, UUID
import os
from pathlib import Path

app = Quart(__name__)

files = {}  

# Load SECRET_UUID from environment or from a .env file in the project root.
# If none exists, generate one and persist it into .env for subsequent runs.
def _load_or_create_secret_uuid_env(env_filename: str = '.env'):
    project_root = Path(__file__).resolve().parent.parent
    env_path = project_root / env_filename

    # helper: ensure .env contains SECRET_UUID=the_value (replace or append)
    def _ensure_env_contains(path: Path, the_value: str):
        try:
            if path.exists():
                text = path.read_text()
                lines = text.splitlines()
                found = False
                for i, line in enumerate(lines):
                    if line.strip().startswith('SECRET_UUID='):
                        lines[i] = f'SECRET_UUID={the_value}'
                        found = True
                        break
                if not found:
                    # append
                    if not text.endswith('\n') and len(text) > 0:
                        text = text + '\n'
                    text = text + f'SECRET_UUID={the_value}\n'
                else:
                    text = '\n'.join(lines) + '\n'
                path.write_text(text)
            else:
                path.write_text(f'SECRET_UUID={the_value}\n')
        except Exception:
            # ignore persistence errors
            pass

    # 1) environment variable has priority
    env_val = os.environ.get('SECRET_UUID')
    if env_val:
        try:
            secret = UUID(env_val)
            # ensure .env mirrors environment value for future runs
            _ensure_env_contains(env_path, str(secret))
            return secret
        except Exception:
            # invalid env format -> continue to file lookup/generate
            pass

    # 2) look for .env in project root
    if env_path.exists():
        try:
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                key, val = line.split('=', 1)
                if key.strip() == 'SECRET_UUID':
                    try:
                        secret = UUID(val.strip())
                        # export into process env for immediate use
                        os.environ['SECRET_UUID'] = str(secret)
                        return secret
                    except Exception:
                        break
        except Exception:
            pass

    # 3) generate, persist into .env and export
    new_uuid = uuid4()
    _ensure_env_contains(env_path, str(new_uuid))
    os.environ['SECRET_UUID'] = str(new_uuid)
    return new_uuid

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