from quart import Quart, jsonify, request
from uuid import uuid4, uuid5
from hashlib import sha256, sha1

app = Quart(__name__)

users = {}
secret_uuid = uuid4()

@app.put('/user')
async def user():
    data = await request.get_json()
    user = data.get("name")
    password = data.get("password")
    
    #vacio?
    if not data or not user or "password" not in data:
        return jsonify({"error": "Faltan parámetros requeridos"}), 400
    
    #comprobar si ya existe
    if (user in users):
        return jsonify({"error": "El usuario ya existe"}), 409
    
    #crear uid y token de este usuario
    user_uid = str(uuid4())
    token = str(uuid5(secret_uuid, user_uid))
    
    
if __name__ == '__main__':
    app.run(host='localhost', port=5050)



"""   curl -X PUT http://127.0.0.1:5050/user \
         -H "Content-Type: application/json" \
         -d '{"name": "alice", "password": "mi_password"}'
"""