# PRÁCTICA 1: README

# Nota: Todos los comandos deben ejecutarse en el directorio raíz del proyecto. 

# OPCIÓN A: EJECUCIÓN CON DOCKER COMPOSE
# Para construir imagen y levantar ambos microservicios:
docker compose up --build
# Para detener servicios:
docker compose down

# OPCIÓN B: EJECUCIÓN EN ENTORNO LOCAL
# En una terminal ejecutar (servicio de usuarios):
mkdir -p venv/si1p1
python3 -m venv venv/si1p1
source ./venv/si1p1/bin/activate
pip install -r requirements.txt
hypercorn src.user:app --bind 0.0.0.0:5050
# En otra terminal ejecutar (servicio de archivos):
source ./venv/si1p1/bin/activate
hypercorn src.file:app --bind 0.0.0.0:5051
# Para detener los microservicios basta con hacer CTRL + C en ambas terminales

# En ambas terminales el entorno virtual se desactiva con:
deactivate

# EJECUTAR EL CLIENTE DE PRUEBA
python3 cliente.py