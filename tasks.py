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
def create_person(self, body):
    # pesquisa pessoa
    response = requests.get(
        f'{BASE_PIPEDRIVE}/persons/search', 
        params={
            'api_token': f'{API_KEY}',
            'fields': 'custom_fields',
            'term': body['5393d60f6fce8d6992306d1ab458011f661465c8']
        }, 
        json=body)

    if response.status_code != 200:
        raise ValueError(response.text)

    if not response.json()['data']['items']:
        
        response = requests.post(f'{BASE_PIPEDRIVE}/persons', params={'api_token': f'{API_KEY}'}, json=body)
    
        if not response.ok:
            raise ValueError(response.text)

        if response.status_code == 201:
            title = response.json()['data']['name']
            owner_id = response.json()['data']['owner_id']['id']
            person_id = response.json()['data']['id']

    print('Pessoa já cadastrada')

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
def create_lead(self, body):
    
    if body is not None:
        
        response = requests.post(f'{BASE_PIPEDRIVE}/leads', params={'api_token': f'{API_KEY}'}, json=body)
    
        if not response.ok:
            raise ValueError(response.text)

        if response.status_code == 201:
            return response.json()


