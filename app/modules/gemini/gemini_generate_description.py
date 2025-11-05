import google.generativeai as genai
from config import settings
import json
from . import gemini_create_log as log

# Configuração da API do Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)  # Insira sua API key aqui
model = genai.GenerativeModel("gemini-2.5-pro")


def gerar_descricao(sku, nome="", marca="", ean="", cod_fabricante="", debug=False):
    """
    Gera nome, descrição, ficha técnica e metadescrição (SEO) do produto.
    Mostra prompt enviado se debug=True.
    """
    prompt = f"""
Gere informações detalhadas do produto usando os dados fornecidos.
Siga exatamente o formato abaixo:

Nome: nome claro e organizado do produto (≤70 caracteres). Formato: [nome][modelo, caso tenha][marca][cód. fab]
Marca:
Descrição: Breve introdução sobre o produto (até 250 caracteres)
Escopos: 3 escopos do produto, divida em itens.
Ficha técnica: Lista de pares chave/valor com dados como marca, tamanho, modelo, material, capacidade. Não invente dados técnicos; use apenas dados contidos no prompt.
Sugestões de uso: lista com até 3 sugestões, divida em itens.
Mais sobre o Produto: Descrição complementar sobre o produto, (Até 300 caracteres)
Metadescrição: descrição resumida em até 160 caracteres.


Dados do produto:
Nome: {nome}
Marca: {marca}
EAN: {ean}
codigo do fabricante:{cod_fabricante}

Responda em JSON, com os campos: nome, marca, descricao, escopos, ficha_tecnica, sugestoes_de_uso, mais_sobre_o_produto, metadescricao.
No conteúdo dos campos, utilize apenas textos simples, sem markdown, emojis ou caracteres especiais além da pontuação adequada.
O EAN e o codigo do fabricante não devem aparecer no seu texto.
"""

    if debug:
        print("🧠 PROMPT ENVIADO PARA O GEMINI:")
        print(prompt)
        print("=" * 80)

    # Chamada à API
    response = model.generate_content(prompt)
    texto = response.text

    # 🧹 Remove os delimitadores do bloco de código
    if texto.startswith("```"):
        # remove ```json ou ``` no início e ``` no final
        texto = texto.strip().strip("`")
        texto = texto.replace("json", "", 1).strip()

    log.salvar_conteudo(sku=sku, conteudo=texto)
    conteudo = json.loads(texto)

    return conteudo