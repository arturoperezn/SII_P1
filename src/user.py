from quart import Quart, jsonify, request
from uuid import uuid4, uuid5, UUID
import os
from pathlib import Path
from hashlib import sha256, sha1

app = Quart(__name__)

# source .venv/bin/activate

"""   curl -X PUT http://127.0.0.1:5050/user \
        -H "Content-Type: application/json" \
        -d '{"name": "alice", "password": "mi_password"}'
"""

users = {}


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

# Función aux para guardar la contraseña encriptada usando SHA-256
def hash_pwd (password: str) -> str:
    #encode lo convierte a bits (sha256 necesita bits), sha256 encripta y hexdigest lo convierte a hex
    return sha256(password.encode()).hexdigest()

# Comprueba si la petición actual trae un token válido de sesión
def check_login():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "): 
        return None
            
    token = token.replace("Bearer ", "")
        
    for user in users.values():
        if user.get("token") == token:
            return user
    return None


# Crea un usuario nuevo con nombre, contraseña y token de acceso
@app.put('/user')
async def create_user():
    
    data = await request.get_json()
    #vacio?
    if not data:
        return jsonify({"error": "Faltan parámetros requeridos"}), 400
        
    name = data.get("name")
    password = data.get("password")
    
    if not name:
            return jsonify({"error": "Falta name"}), 400
    
    if not password:
                return jsonify({"error": "Falta password"}), 400
    
    #comprobar si ya existe
    if (name in users):
        return jsonify({"error": "El usuario ya existe"}), 409
    
    #crear uid y token de este usuario
    user_uid = str(uuid4())
    pwd_hash = hash_pwd(password)
    token = str(uuid5(secret_uuid, user_uid))
    
    users[name] = {
        "uid": user_uid,
        "pwd_hash": pwd_hash,
        "token": token
    }
    
    return jsonify({
        "uid": user_uid,
        "token": token
    }), 201

    


# Inicia sesión comprobando nombre y contraseña y devuelve el token
@app.post("/user")
async def login():
    data = await request.get_json()
    if not data:
        return jsonify({"error": "Faltan datos"}), 400
    
    name = data.get("name")
    password = data.get("password")
    
    #comprobamos si el usuario existe
    user = users.get(name)
    if not user:
        return jsonify({"error": "Usuario no existe"}), 404
    
    if user["pwd_hash"] != hash_pwd(password):
        return jsonify({"error": "Password incorrecta"}), 401
    
    return jsonify({
        "uid": user["uid"],
        "token": user["token"]
    })


# Cambia la contraseña del usuario
@app.patch("/user")
async def modify_user():
    #si no esta iniciada la sesion fallar
    user = check_login()
    if not user:
        return jsonify({"error": "No autorizado"}), 401
        
    data = await request.get_json()
    password = data.get("password")
    
    if not password:
        return jsonify ({"error": "Falta nueva password"}), 400
    
    user ["pwd_hash"] = hash_pwd(password)
    return jsonify ({"ok": True})
    
if __name__ == '__main__':
    app.run(host='localhost', port=5050)
