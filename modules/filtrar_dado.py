# app/modules/filtrar_dado.py

def filtrar_por_chave(lista: list, chave: str, valor) -> list:
    return [x for x in lista if x.get(chave) == valor]
