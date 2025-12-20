from datetime import datetime
from modules import ferramentas, magento, categorias
import requests, re, json, csv, os, time
from config import settings

url = settings.NUVEM_PRODUCTS_API
bearer = settings.NUVEM_BEARER
user_agent = settings.NUVEM_USER_AGENT
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def is_vazio(valor):
    return valor == ""

def medida_invalida(valor):
    return (
        valor in (0, "0", 0.0)
        or (isinstance(valor, str) and "," in valor)
    )

def log(mensagem, sku):
    ferramentas.logger.novo_log(mensagem=mensagem, base_dir=timestamp, sku=sku)

def append_csv(sku: str, id_nuvemshop: str, retorno: str):
    arquivo=f".ignorables/migracoes/{timestamp}.csv"
    existe = os.path.isfile(arquivo)

    with open(arquivo, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not existe:
            writer.writerow(["sku", "id_nuvemshop", "retorno"])

        writer.writerow([sku, id_nuvemshop, retorno])

def importar(sku: str):

    log(mensagem="Importação iniciada.", sku=sku)
    print(f"[{sku}] Importação iniciada.")
    
    #Pega JSON do magento
    produto = magento.get_produto(sku)
    log(mensagem=f"Retorno magento recebido.\n\n{produto}", sku=sku)
    print(f"[{sku}] Retorno magento recebido.")

    # ---------- ERRO NO GET ----------
    if isinstance(produto, dict) and "erro" in produto:
        retorno = {"sku": sku, "status": "erro_magento", "detalhe": produto["erro"]}
        append_csv(sku=sku, id_nuvemshop="", retorno=retorno)
        log(mensagem=f"Fim da execução.\n\n{retorno}", sku=sku)
        return retorno

    # ---------- DADOS BÁSICOS ----------
    nome = produto.get("name", "")
    status = True if produto.get("status") == 1 else False
    price = produto.get("price", 0)
    weight = produto.get("weight", "0")

    stock = (produto.get("extension_attributes", {}).get("stock_item", {}).get("qty", 0))

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
        if id_nuvem == "":
            retorno = {"sku": sku, "status": "erro_categoria", "detalhe": "Categorize o produto dentro da nova árvore e tente novamente."}
            append_csv(sku=sku, id_nuvemshop="", retorno=retorno)
            log(mensagem=f"Fim da execução.\n\n{retorno}", sku=sku)
            return retorno
    
    promotional_price = custom.get("special_price", "")
    descricao = re.sub(r'\s*(style|border)="[^"]*"', '', custom.get("description", ""))
    metatitle = custom.get("meta_title", nome)
    metadescription = custom.get("meta_description", "")
    brand = custom.get("manufacturer", "")
    ean = custom.get("ean", "")

    width = custom.get("correios_width", "0")
    height = custom.get("correios_height", "0")
    depth = custom.get("correios_depth", "0")

    validar_medidas = {
        "weight": weight,
        "width": width,
        "height": height,
        "depth": depth,
    }
    
    for campo, valor in validar_medidas.items():
        if medida_invalida(valor):
            retorno = {"sku": sku, "status": "erro_medidas", "detalhe": f"Campo [{campo}] inválido. Não importado."}
            append_csv(sku=sku, id_nuvemshop="", retorno=retorno)
            log(mensagem=f"Fim da execução.\n\n{retorno}", sku=sku)
            return retorno

    # ---------- IMAGENS (máx 9) ----------
    imagens = []
    for img in produto.get("media_gallery_entries", []):
        if len(imagens) >= 9:
            break

        imagens.append({
            "src": f"https://www.ferpam.com.br/media/catalog/product{img['file']}"
        })

    if len(produto.get("media_gallery_entries", [])) > 9:
        print(f"Aviso: SKU {sku} possui mais de 9 imagens. Importação cancelada.")
        retorno = {"sku": sku, "status": "erro_imagens", "detalhe": "Produto com mais de 9 imagens. Não importado"}
        append_csv(sku=sku, id_nuvemshop="", retorno=retorno)
        log(mensagem=f"Fim da execução.\n\n{retorno}", sku=sku)
        return retorno

    # ---------- PRODUTOS RELACIONADOS ----------
    # relacionados = []
    # for link in produto.get("product_links", []):
    #     relacionados.append({
    #         "sku": link["linked_product_sku"],
    #         "type": link["link_type"]
    #     })

    validar_campos = {
        "nome":nome,
        "descricao":descricao,
        "seo_title":metatitle,
        "seo_description":metadescription
    }

    for nomelouco, valorlouco in validar_campos.items():
        if is_vazio(valorlouco):
            retorno = {"sku": sku, "status": "erro_campos", "detalhe": f"Campo [{nomelouco}] inválido. Não importado."}
            append_csv(sku=sku, id_nuvemshop="", retorno=retorno)
            log(mensagem=f"Fim da execução.\n\n{retorno}", sku=sku)
            return retorno

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
        }],
        "published": status,
        "images": imagens,
        "categories": categories
    }
    log(mensagem=f"Payload montado.\n\n{payload}", sku=sku)
    print(f"[{sku}] Payload Pronto. Enviando para Nuvemshop...")

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
        log(mensagem=f"Resposta nuvemshop recebida.\n\n{resp.text}", sku=sku)

        if resp.status_code not in (200, 201):
            retorno = {"sku": sku, "status": "erro_nuvemshop", "detalhe": f"[{resp.status_code}] {resp.text}"}
            append_csv(sku=sku, id_nuvemshop="", retorno=retorno)
            log(mensagem=f"Fim da execução.\n\n{retorno}", sku=sku)
            return retorno
                
        id_nuvemshop = resp.json()["id"]
        retorno = {"sku": sku, "status": "importado_com_sucesso", "detalhe": resp.json()}
        append_csv(sku=sku, id_nuvemshop=id_nuvemshop, retorno=retorno)
        log(mensagem=f"Fim da execução.\n\n{retorno}", sku=sku)
        print(f"[{sku}] Enviado para Nuvemshop com Sucesso.")
        return retorno

    except requests.exceptions.Timeout:
        retorno = {"sku": sku, "status": "erro_nuvemshop", "detalhe": "Timeout no POST"}
        append_csv(sku=sku, id_nuvemshop="", retorno=retorno)
        log(mensagem=f"Fim da execução.\n\n{retorno}", sku=sku)
        return retorno
    except requests.exceptions.ConnectionError:
        retorno = {"sku": sku, "status": "erro_nuvemshop", "detalhe": "Falha de conexão"}
        append_csv(sku=sku, id_nuvemshop="", retorno=retorno)
        log(mensagem=f"Fim da execução.\n\n{retorno}", sku=sku)
        return retorno
    except Exception as e:
        retorno = {"sku": sku, "status": "erro", "detalhe": str(e)}
        append_csv(sku=sku, id_nuvemshop="", retorno=retorno)
        log(mensagem=f"Fim da execução.\n\n{retorno}", sku=sku)
        return retorno

with open("teste.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # time.sleep(3)
        importado = importar(row["sku"])
        print(f"[{importado["sku"]}] Status: {importado["status"]}")