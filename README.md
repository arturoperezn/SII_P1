# Microservicio usersvc

Instalar deps:
pip install -r requirements.txt

Ejecutar local:
hypercorn user:app --bind 0.0.0.0:5050

Docker:

docker build -t usersvc .
docker run -p 5050:5050 usersvc

o con docker-compose:
sudo docker-compose up --build