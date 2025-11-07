import requests
import json
from config import settings

def put_produto(
        sku: str,
        nome: str = None,
        descricao: str = None,
        aplicacao: str = None,
        dadosTecnicos: str = None,
        itensInclusos: str = None,
        altura: str = None,
        largura: str = None,
        profundidade: str = None
        ):

    url = f"{settings.AUTCOM_PATCHPRODUCT_PATH}{sku}"

    # monta o payload só com o que foi informado
    payload_dict = {
        "nome": nome,
        "descricao": descricao,
        "aplicacao": aplicacao,
        "dadosTecnicos": dadosTecnicos,
        "itensInclusos": itensInclusos,
        "altura": altura,
        "largura": largura,
        "profundidade": profundidade,
    }

    # remove chaves com valor None
    payload = json.dumps({k: v for k, v in payload_dict.items() if v is not None})

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {settings.AUTCOM_WS_AUTH}'
    }

    response = requests.patch(url, headers=headers, data=payload)
    return response