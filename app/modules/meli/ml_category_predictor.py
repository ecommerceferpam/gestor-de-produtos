import requests
from . import ml_token

def buscar_categoria(query):

    access_token = ml_token.get_meli_token()

    url = f"https://api.mercadolibre.com/sites/MLB/domain_discovery/search?limit=3&q={query}"
    payload = {}
    headers = {
    'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text