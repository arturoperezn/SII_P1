# PRÁCTICA 1: README
Instalar deps:
pip install -r requirements.txt

Docker-compose:
sudo docker-compose up --build

Ejecutar local:
hypercorn src.user:app --bind 0.0.0.0:5050
hypercorn src.file:app --bind 0.0.0.0:5051

pruebas: 
python3 cliente.py