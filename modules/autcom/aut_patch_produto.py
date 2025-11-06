import requests
import json
from config import settings


def put_produto(
        sku: str,
        altura,
        aplicacao,
        categorias,
        dadosTecnicos,
        descricao,
        destaque,
        i
        ):
    url = f"{settings.AUTCOM_PATCHPRODUCT_PATH}{sku}"

    payload = json.dumps({
    "altura": 100,
    "aplicacao": "teste arthur dnv aplicacao",
    "categorias": "teste arthur categorias",
    "dadosTecnicos": "teste arthur dados técnicos",
    "descricao": "teste arthur descricao",
    "destaque": False,
    "itensInclusos": "teste arthur itens inclusos",
    "largura": 99,
    "nome": "teste arthur nome",
    "profundidade": 98,
    "urlImagem": "teste arthur url"
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {settings.AUTCOM_WS_AUTH}'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)

    return response