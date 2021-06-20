from fastapi import FastAPI, Request
from tasks import create_lead, create_person
from celery import chain
import json

app = FastAPI()


@app.post("/cretae_lead")
async def create_person_pipdrive(request: Request):
    
    json = await request.json()

    nome = json['leads'][0]['name']
    email = json['leads'][0]['email']
    uuid = json['leads'][0]['uuid']
    telefone = json['leads'][0]['personal_phone']

    body = {
        "name": nome,
        "phone": [
            {
            "label": "work",
            "value": telefone,
            "primary": True
            }
        ],
        "email": [
            {
            "label": "work",
            "value": email,
            "primary": True
            }
        ],
        "5393d60f6fce8d6992306d1ab458011f661465c8": uuid
    }

    #create_lead.delay(body)
    task_id = chain(
        create_person.s(body),
        create_lead.s(),)()
    
     
@app.get("/callback")
async def callback(request: Request):
    print(await request.json())