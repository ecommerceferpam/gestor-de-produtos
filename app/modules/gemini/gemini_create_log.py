import json
import os
from datetime import datetime

def salvar_conteudo(sku, conteudo, pasta="logs"):
    # Diretório onde o script está salvo (independente de onde for executado)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Caminho completo da pasta de destino
    pasta_destino = os.path.join(base_dir, pasta)
    
    # Garante que a pasta existe (cria se não existir)
    os.makedirs(pasta_destino, exist_ok=True)

    # Gera timestamp (ex: 2025-11-04_14-38-50)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Define o caminho completo do arquivo
    nome_arquivo = os.path.join(pasta_destino, f"{sku}_{timestamp}.json")


    # 🔍 Se for string JSON, converte para dict antes de salvar
    if isinstance(conteudo, str):
        try:
            conteudo = json.loads(conteudo)
        except json.JSONDecodeError:
            pass  # deixa como string se não for JSON válido


    # Salva o conteúdo em formato JSON legível
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(conteudo, f, ensure_ascii=False, indent=4)
    
    return nome_arquivo  # opcional, mas útil

def carregar_conteudo(nome_arquivo):
    # Lê o arquivo e converte de volta para dicionário
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        conteudo = json.load(f)
    return conteudo
