import requests
import json
from config import settings

def buscar_dados_produto(sku):

    """
    Busca os dados de um produto no Magento via API REST.
    Retorna um dict com os dados do produto ou um dict de erro.
    """

    # url = f"https://www.ferpam.com.br/rest/V1/products?searchCriteria[filter_groups][0][filters][0][field]=sku&searchCriteria[filter_groups][0][filters][0][value]={sku}&searchCriteria[filter_groups][0][filters][0][condition_type]=eq"

    url = f"https://www.ferpam.com.br/rest/V1/products/{sku}"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {settings.MAGENTO_API_KEY}',
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 404:
            return {"erro": f"Produto com SKU '{sku}' não encontrado (404)."}
        elif response.status_code == 401:
            return {"erro": "Não autorizado. Verifique o token Bearer."}
        elif response.status_code != 200:
            return {"erro": f"Erro HTTP {response.status_code}: {response.text}"}

        try:
            data = response.json()
        except json.JSONDecodeError:
            return {"erro": "Erro ao decodificar resposta JSON da API."}

        # ✅ Retorna os dados do produto
        return data

    except requests.exceptions.Timeout:
        return {"erro": "A requisição demorou demais e foi encerrada (timeout)."}
    except requests.exceptions.ConnectionError:
        return {"erro": "Falha de conexão com o servidor do Magento."}
    except Exception as e:
        return {"erro": f"Ocorreu um erro inesperado: {str(e)}"}