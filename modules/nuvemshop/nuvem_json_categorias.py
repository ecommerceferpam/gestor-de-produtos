import json
from copy import deepcopy
from modules import nuvemshop


def criar_categorias_nuvemshop(categorias_json: list):
    """
    Lê o JSON de categorias, cria categorias na Nuvemshop respeitando hierarquia
    e retorna um NOVO JSON com id_nuvemshop preenchido.
    """

    categorias = deepcopy(categorias_json)

    # índice rápido por id
    index = {}

    def indexar(cat):
        index[cat["id"]] = cat
        for filho in cat.get("children", []):
            indexar(filho)

    for raiz in categorias:
        indexar(raiz)

    # ---------- LOOP POR LEVEL ----------
    level = 0
    while True:
        nivel_atual = [
            cat for cat in index.values()
            if cat.get("level") == level
        ]

        if not nivel_atual:
            break

        for cat in nivel_atual:
            # já criada
            if "id_nuvemshop" in cat:
                continue

            parent_nuvemshop_id = None

            if cat.get("parent_id"):
                parent = index.get(cat["parent_id"])
                parent_nuvemshop_id = parent.get("id_nuvemshop")

            # cria categoria
            id_nuvem = nuvemshop.nova_categoria(
                cat["name"],
                parent=parent_nuvemshop_id
            )

            # atualiza JSON
            cat["id_nuvemshop"] = id_nuvem

        level += 1

    return categorias

# Pode executar em main.py
def massa():
    with open("taxonomy_tree.json", "r", encoding="utf-8") as f:
        categorias = json.load(f)

    resultado = nuvemshop.json_para_categorias(categorias)

    with open("categorias_nuvemshop.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)