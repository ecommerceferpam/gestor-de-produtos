def get_field(produto: dict, path: str, default: str = "") -> str:
    """
    Retorna o valor de um campo do produto, suportando paths com '>'.
    Ex.: path = "marca>descricao"
    """
    keys = path.split(">")

    value = produto
    for key in keys:
        if not isinstance(value, dict):
            return default
        value = value.get(key)

    return str(value) if value is not None else default


# ============================
# Funções específicas
# ============================

def get_descricao(produto: dict) -> str:
    return get_field(produto, "descricao")

def get_dados_tecnicos(produto: dict) -> str:
    return get_field(produto, "dadosTecnicos")

def get_aplicacao(produto: dict) -> str:
    return get_field(produto, "aplicacao")

def get_altura(produto: dict) -> str:
    return get_field(produto, "altura")

def get_largura(produto: dict) -> str:
    return get_field(produto, "largura")

def get_profundidade(produto: dict) -> str:
    return get_field(produto, "profundidade")

def get_itens_inclusos(produto: dict) -> str:
    return get_field(produto, "itensInclusos")

def get_nome(produto: dict) -> str:
    return get_field(produto, "nome")

def get_codigo_barra(produto: dict) -> str:
    return get_field(produto, "codigoBarra")

def get_descricao_cadastro(produto: dict) -> str:
    return get_field(produto, "descricaoCadastro")

def get_classificacao_ipi(produto: dict) -> str:
    return get_field(produto, "classificacaoIPI")

def get_ativo(produto: dict) -> str:
    return get_field(produto, "ativo")

def get_marca_descricao(produto: dict) -> str:
    return get_field(produto, "marca>descricao")

def get_cod_fab(produto: dict) -> str:
    return get_field(produto, "codigoFabrica")