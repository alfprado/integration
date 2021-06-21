from worker import celery_app
import requests
from requests.exceptions import RequestException

API_KEY = '6180028d1e71985ae8e3106afcb3805cf3dc1290'
BASE_PIPEDRIVE = 'https://api.pipedrive.com/v1'

@celery_app.task(
    bind=True,
    max_retry=5,
    retry_backoff=True,
    autoretry_for=(RequestException,)
    )
def create_person(self, data):

    # pesquisa pessoa
    response = requests.get(
        f'{BASE_PIPEDRIVE}/persons/search', 
        params={
            'api_token': f'{API_KEY}',
            'fields': 'email',
            'term': data['email']
        })

    if response.status_code != 200:
        raise ValueError(response.text)

    if not response.json()['data']['items']:
        
        person = {
            "name": data['nome'],
            "phone": [
                {
                "label": "work",
                "value": data['telefone'],
                "primary": True
                }
            ],
            "email": [
                {
                "label": "work",
                "value": data['email'],
                "primary": True
                }
            ],
            "5393d60f6fce8d6992306d1ab458011f661465c8": data['uuid']
        }
        
        response = requests.post(f'{BASE_PIPEDRIVE}/persons', params={'api_token': f'{API_KEY}'}, json=person)
    
        if not response.ok:
            raise ValueError(response.text)

        if response.status_code == 201:
           
            person_id = response.json()['data']['id']
            title = response.json()['data']['name']
            owner_id = response.json()['data']['owner_id']['id']
            
            return {
                    "title": title,
                    "owner_id": owner_id,
                    "person_id": person_id
                }
    
    person_id = response.json()['data']['items'][0]['item']['id']
    title = response.json()['data']['items'][0]['item']['name']
    owner_id = response.json()['data']['items'][0]['item']['owner']['id']
    
    return {
            "title": title,
            "owner_id": owner_id,
            "person_id": person_id
        }

@celery_app.task(
    bind=True,
    max_retry=5,
    retry_backoff=True,
    autoretry_for=(RequestException,)
    )
def create_lead(self, data):
    
    if data is not None:
        
        response = requests.post(f'{BASE_PIPEDRIVE}/leads', params={'api_token': f'{API_KEY}'}, json=data)
    
        if not response.ok:
            raise ValueError(response.text)

        if response.status_code == 201:
            return response.json()
    
    
@celery_app.task(
    bind=True,
    max_retry=5,
    retry_backoff=True,
    autoretry_for=(RequestException,)
    )
def update_person(self, data):

    # pesquisa pessoa
    response = requests.get(
        f'{BASE_PIPEDRIVE}/persons/search', 
        params={
            'api_token': f'{API_KEY}',
            'fields': 'email',
            'term': data['email']
        })

    if response.status_code != 200:
        raise ValueError(response.text)
    
    person_id = response.json()['data']['items'][0]['item']['id']

    person = {
        '7f1af98bb50f52f042f0d72f1c7b9cb8089b3817': data['endereco'],
        'af83a47de2c3d257054a6746018176671c139c4f': data['profissao'],
        '1934121a8b8b398f6015fc28697a1b2b187ed2b9': data['documento']
    }
        
    response = requests.put(f'{BASE_PIPEDRIVE}/persons/{person_id}', params={'api_token': f'{API_KEY}'}, json=person)

    if not response.ok:
        raise ValueError(response.text)

    if response.status_code == 200:
        return response.json()