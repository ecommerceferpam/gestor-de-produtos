import requests
import json
from config import settings

def get_produto(sku: str):
    url = f"{settings.AUTCOM_GETPRODUCT_PATH}{sku}"

    payload = {}
    headers = {
    'Authorization': f'Basic {settings.AUTCOM_WS_AUTH}'
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 404:
            return {"erro": f"Produto com SKU '{sku}' não encontrado (404)."}
        elif response.status_code == 401:
            return {"erro": "Não autorizado. Verifique o token Bearer."}
        elif response.status_code != 200:
            return {"erro": f"Erro HTTP {response.status_code}: {response.text}"}

        try:
            conteudo = json.loads(response.text)
        except json.JSONDecodeError:
            return {"erro": "Erro ao decodificar resposta JSON da API."}

        # ✅ Retorna os dados do produto
        return conteudo

    except requests.exceptions.Timeout:
        return {"erro": "A requisição demorou demais e foi encerrada (timeout)."}
    except requests.exceptions.ConnectionError:
        return {"erro": "Falha de conexão com o servidor do Magento."}
    except Exception as e:
        return {"erro": f"Ocorreu um erro inesperado: {str(e)}"}