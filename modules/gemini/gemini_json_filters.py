
def extrair_nome(json_data):
    return json_data.get("nome", "Campo 'nome' não encontrado")

def extrair_marca(json_data):
    return json_data.get("marca", "Campo 'marca' não encontrado")

def extrair_descricao(json_data):
    return json_data.get("descricao", "Campo 'descricao' não encontrado")

def extrair_metadescricao(json_data):
    return json_data.get("metadescricao", "Campo 'metadescricao' não encontrado")