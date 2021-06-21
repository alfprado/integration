# Instalação

$ pip install -r requirements.txt

## Inicia o broker
docker-compose up -d

## Inicia a Api
$ uvicorn main:app --reload

## Inicia o worker 
$ celery -A worker worker --loglevel=INFO

## Inicia o flower
$ celery flower -A worker --broker:pyamqp://guest@localhost

http://localhost:8000/docs
http://localhost:5555