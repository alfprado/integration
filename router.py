from fastapi import Request, APIRouter
from tasks import create_lead, create_person, update_person
from celery import chain
import json

router = APIRouter()

@router.post("/create_lead")
async def create_person_pipdrive(request: Request):
    
    json = await request.json()

    nome = json['leads'][0]['name']
    email = json['leads'][0]['email']
    uuid = json['leads'][0]['uuid']
    telefone = json['leads'][0]['personal_phone']

    data = {'nome': nome, 'email': email, 'uuid': uuid, 'telefone': telefone}

    task_id = chain(
        create_person.s(data),
        create_lead.s(),)()

@router.post('/update_person')
async def update_person_pipdrive(request: Request):

    json = await request.json()
    
    email = json['leads'][0]['email']
    uuid = json['leads'][0]['uuid']
    profissao = json['leads'][0]['last_conversion']['content']['Profissão']
    endereco = json['leads'][0]['last_conversion']['content']['Endereço']
    documento = json['leads'][0]['last_conversion']['content']['Documento']
    
    data = {
        'email': email, 
        'uuid': uuid, 
        'profissao': profissao,
        'endereco': endereco, 
        'documento': documento
    }
    
    task_id = update_person.delay(data)