# app/modules/buscar_produto.py

def buscar_por_id(product_id: int) -> dict:
    # implemente sua lógica real aqui
    fake_db = {1: {"id":1, "nome":"Teclado"}, 2: {"id":2, "nome":"Mouse"}}
    return fake_db.get(product_id, {})

def buscar_por_nome(nome: str, limit: int = 10) -> list:
    # lógica de busca
    items = [{"id":1,"nome":"Teclado"}, {"id":2,"nome":"Mouse"}]
    return [i for i in items if nome.lower() in i["nome"].lower()][:limit]
