from quart import Quart, jsonify, request
from uuid import uuid4, uuid5
from hashlib import sha256, sha1

app = Quart(__name__)

# source .venv/bin/activate

"""   curl -X PUT http://127.0.0.1:5050/user \
        -H "Content-Type: application/json" \
        -d '{"name": "alice", "password": "mi_password"}'
"""

users = {}
secret_uuid = uuid4()

# Función aux para guardar la contraseña encriptada usando SHA-256
def hash_pwd (password: str) -> str:
    #encode lo convierte a bits (sha256 necesita bits), sha256 encripta y hexdigest lo convierte a hex
    return sha256(password.encode()).hexdigest()

# Comprueba si la petición actual trae un token válido de sesión
def check_login():
    token = request.headers.get("Authorization")
    if not token: 
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

    
if __name__ == '__main__':
    app.run(host='localhost', port=5050)
    

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
        return jsonify({"error": "Contraseña incorrecta"}), 401
    
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
    