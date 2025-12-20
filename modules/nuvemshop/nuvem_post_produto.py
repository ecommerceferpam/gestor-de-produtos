import requests
import json
from config import settings

url = settings.NUVEM_PRODUCTS_API
bearer = settings.NUVEM_BEARER
user_agent = settings.NUVEM_USER_AGENT
# price = "10.00"
# stock = 12
# weight = "2.000"
# width = "0.00"
# status = True or False

def post_produto(sku, status, nome, descricao, metatitle, metadescription, brand, price, promotional_price, stock, weight, width, height, depth, ean):

    payload = json.dumps({
    "name": {
        "pt": f"{nome}"
    },
    "description": {
        "pt": f"{descricao}"
    },
    "seo_title": {
        "pt": f"{metatitle}"
    },
    "seo_description": {
        "pt": f"{metadescription}"
    },
    "brand": f"{brand}",
    "variants": [
        {
        "price": f"{price}",
        "promotional_price": f"{promotional_price}",
        "stock_management": True,
        "stock": stock,
        "weight": f"{weight}",
        "width": f"{width}",
        "height": f"{height}",
        "depth": f"{depth}",
        "sku": f"{sku}",
        "barcode": f"{ean}",
        "visible": status
        }
    ],
    "images": [
        {
        "src": "https://www.ferpam.com.br/media/catalog/product/j/o/jogo_de_ferramentas_3.jpg"
        }
    ],
    "categories": []
    })
    headers = {
    'Authentication': f'bearer {bearer}',
    'User-Agent': f'{user_agent}',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)