import requests
import json
from modules import magento,categorias
from config import settings
import re

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


def importar_produto_por_sku(sku: str):

    #Pega JSON do magento
    produto = magento.get_produto(sku)

    # ---------- ERRO NO GET ----------
    if isinstance(produto, dict) and "erro" in produto:
        return {
            "sku": sku,
            "status": "erro_magento",
            "detalhe": produto["erro"]
        }

    # ---------- DADOS BÁSICOS ----------
    nome = produto.get("name", "")
    status = True if produto.get("status") == 1 else False
    price = produto.get("price", 0)
    weight = produto.get("weight", "0")

    stock = (
        produto.get("extension_attributes", {})
               .get("stock_item", {})
               .get("qty", 0)
    )

    # ---------- CUSTOM ATTRIBUTES ----------
    custom = {
        a["attribute_code"]: a["value"]
        for a in produto.get("custom_attributes", [])
    }
    
    category_ids = custom.get("category_ids", [])

    # ---------- CATEGORIAS ----------
    categories = []

    for cat_id in category_ids:
        id_nuvem = categorias.busca_idnuvem(cat_id)
        if id_nuvem != "":
            categories.append(id_nuvem)

    
    promotional_price = custom.get("special_price", "")
    # descricao = custom.get("description", "")
    # descricao = re.sub(r'\s*style="[^"]*"', '', custom.get("description", ""))
    descricao = re.sub(r'\s*(style|border)="[^"]*"', '', custom.get("description", ""))
    metatitle = custom.get("meta_title", nome)
    metadescription = custom.get("meta_description", "")
    brand = custom.get("manufacturer", "")
    ean = custom.get("ean", "")

    width = custom.get("correios_width", "0")
    height = custom.get("correios_height", "0")
    depth = custom.get("correios_depth", "0")

    # ---------- IMAGENS (máx 9) ----------
    imagens = []
    for img in produto.get("media_gallery_entries", []):
        if len(imagens) >= 9:
            break

        imagens.append({
            "src": f"https://www.ferpam.com.br/media/catalog/product{img['file']}"
        })

    if len(produto.get("media_gallery_entries", [])) > 9:
        print(f"Aviso: SKU {sku} possui mais de 9 imagens. Excedentes ignoradas.")

    # ---------- PRODUTOS RELACIONADOS ----------
    # relacionados = []
    # for link in produto.get("product_links", []):
    #     relacionados.append({
    #         "sku": link["linked_product_sku"],
    #         "type": link["link_type"]
    #     })

    # ---------- PAYLOAD CLOUD ----------
    payload = {
        "name": {"pt": nome},
        "description": {"pt": descricao},
        "seo_title": {"pt": metatitle},
        "seo_description": {"pt": metadescription},
        "brand": brand,
        "variants": [{
            "price": str(price),
            "promotional_price": str(promotional_price),
            "stock_management": True,
            "stock": stock,
            "weight": str(weight),
            "width": str(width),
            "height": str(height),
            "depth": str(depth),
            "sku": sku,
            "barcode": str(ean),
            "published": status
        }],
        "images": imagens,
        # "related_products": relacionados,
        "categories": categories
    }
    # print(payload)

    headers = {
        "Authentication": f"bearer {bearer}",
        "User-Agent": user_agent,
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=15
        )

        if resp.status_code not in (200, 201):
            return {
                "sku": sku,
                "status": "erro_cloud",
                "http_code": resp.status_code,
                "detalhe": resp.text
            }

        return {
            "sku": sku,
            "status": "importado_com_sucesso",
            "cloud_response": resp.json()
        }

    except requests.exceptions.Timeout:
        return {"sku": sku, "status": "erro_cloud", "detalhe": "Timeout no POST"}
    except requests.exceptions.ConnectionError:
        return {"sku": sku, "status": "erro_cloud", "detalhe": "Falha de conexão"}
    except Exception as e:
        return {"sku": sku, "status": "erro_cloud", "detalhe": str(e)}
