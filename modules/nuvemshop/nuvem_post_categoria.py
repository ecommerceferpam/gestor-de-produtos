import requests
import json
from config import settings

def post_categoria(nome, parent):
    url = settings.NUVEM_CATEGORIES_API

    payload = json.dumps({
    "name": {
        "pt": f"{nome}"
    },
    "parent": parent
    })
    headers = {
    'Authentication': f'bearer {settings.NUVEM_BEARER}',
    'User-Agent': f'{settings.NUVEM_USER_AGENT}',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = json.loads(response.text)
    # print(response.text)
    return data['id']
