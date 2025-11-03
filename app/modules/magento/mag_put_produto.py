import requests
import json
from config import settings

def enviar_dados_produto(
        sku, 
        nome=None, 
        peso=None, 
        descricao=None, 
        metaTitle=None, 
        metaDescription=None, 
        altura=None, 
        largura=None, 
        profundidade=None
):
    # --- Validação do SKU ---
    if not sku or not str(sku).strip():
        raise ValueError("O parâmetro 'sku' é obrigatório e não pode ser vazio.")
    
    # --- Checar se há ao menos um outro parâmetro informado ---
    outros_campos = [nome, peso, descricao, metaTitle, metaDescription, altura, largura, profundidade]
    if not any(outros_campos):
        raise ValueError("É necessário informar ao menos um parâmetro além do SKU.")
    
    url = f"https://www.ferpam.com.br/rest/V1/products/{sku}"

    # --- Montar payload dinâmico ---
    product_data = {"sku": str(sku).strip()}
    
    if nome:
        product_data["name"] = nome
    if peso:
        product_data["weight"] = peso

    custom_attributes = []
    if descricao:
        custom_attributes.append({"attribute_code": "description", "value": descricao})
    if metaTitle:
        custom_attributes.append({"attribute_code": "meta_title", "value": metaTitle})
    if metaDescription:
        custom_attributes.append({"attribute_code": "meta_description", "value": metaDescription})
    if altura:
        custom_attributes.append({"attribute_code": "correios_height", "value": str(altura)})
    if largura:
        custom_attributes.append({"attribute_code": "correios_width", "value": str(largura)})
    if profundidade:
        custom_attributes.append({"attribute_code": "correios_depth", "value": str(profundidade)})

    if custom_attributes:
        product_data["custom_attributes"] = custom_attributes
    
    payload = json.dumps({"product": product_data}, ensure_ascii=False)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.MAGENTO_API_KEY}'  # <-- coloque seu token aqui
    }

    try:
        response = requests.put(url, headers=headers, data=payload)

        if response.status_code in (200, 201):
            print(f"✅ Produto {sku} atualizado com sucesso!")
        elif response.status_code == 404:
            print(f"⚠️ Produto {sku} não encontrado no Magento.")
        elif response.status_code == 401:
            print("🚫 Erro de autenticação: token inválido ou expirado.")
        else:
            try:
                error_msg = response.json().get("message", "")
            except:
                error_msg = response.text
            print(f"❌ Erro {response.status_code}: {error_msg}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")