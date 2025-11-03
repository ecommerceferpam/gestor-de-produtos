def filter_descricao(data):
    """
    Recebe um dict e retorna o campo "description".
    """
    for attr in data["custom_attributes"]:
        if attr["attribute_code"] == "description":
            return attr["value"]
        
def filter_nome(data):

    """
    Recebe um dict e retorna o campo "name".
    """
    return data["name"]

def filter_createdAt(data):
    return data["created_at"]

def filter_updatedAt(data):
    return data["updated_at"]

def filter_sku(data):
    return data["sku"]

def filter_ean(data):
    """
    Recebe um dict e retorna o campo "ean".
    """
    for attr in data["custom_attributes"]:
        if attr["attribute_code"] == "ean":
            return attr["value"]
   
def filter_marca(data):
    """
    Recebe um dict e retorna o campo "brandname".
    """
    for attr in data["custom_attributes"]:
        if attr["attribute_code"] == "brandname":
            return attr["value"]
   
def filter_categoriaGoogle(data):
    """
    Recebe um dict e retorna o campo "google_product_category".
    """
    for attr in data["custom_attributes"]:
        if attr["attribute_code"] == "google_product_category":
            return attr["value"]
   
def filter_conteudoEmbalagem(data):
    """
    Recebe um dict e retorna o campo "conteudo_embalagem".
    """
    for attr in data["custom_attributes"]:
        if attr["attribute_code"] == "conteudo_embalagem":
            return attr["value"]

def filter_peso(data):

    """
    Recebe um dict e retorna o campo "weight".
    """
    return data["weight"]

def filter_largura(data):
    """
    Recebe um dict e retorna o campo "correios_width".
    """
    for attr in data["custom_attributes"]:
        if attr["attribute_code"] == "correios_width":
            return attr["value"]

def filter_altura(data):
    """
    Recebe um dict e retorna o campo "correios_height".
    """
    for attr in data["custom_attributes"]:
        if attr["attribute_code"] == "correios_height":
            return attr["value"]

def filter_comprimento(data):
    """
    Recebe um dict e retorna o campo "correios_depth".
    """
    for attr in data["custom_attributes"]:
        if attr["attribute_code"] == "correios_depth":
            return attr["value"]
        
def filter_metaTitle(data):
    """
    Recebe um dict e retorna o campo "meta_title".
    """
    for attr in data["custom_attributes"]:
        if attr["attribute_code"] == "meta_title":
            return attr["value"]
        
def filter_metaDescription(data):
    """
    Recebe um dict e retorna o campo "meta_description".
    """
    for attr in data["custom_attributes"]:
        if attr["attribute_code"] == "meta_description":
            return attr["value"]
        
def filter_url(data):
    """
    Recebe um dict e retorna o campo "url_key".
    """
    for attr in data["custom_attributes"]:
        if attr["attribute_code"] == "url_key":
            return f"https://www.ferpam.com.br/{attr["value"]}.html"
        