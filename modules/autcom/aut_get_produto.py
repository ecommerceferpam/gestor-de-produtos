import requests
import json
from config import settings

def get_produto(sku: str):
    url = f"{settings.AUTCOM_GETPRODUCT_PATH}{sku}"

    payload = {}
    headers = {
    'Authorization': f'Basic {settings.AUTCOM_WS_AUTH}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    conteudo = json.loads(response.text)
    return conteudo