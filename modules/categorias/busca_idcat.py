import json
from pathlib import Path

# caminho do json no MESMO diretório deste arquivo
_JSON_PATH = Path(__file__).parent / "taxonomy_tree_completo.json"


def buscar_id_nuvemshop_por_id_magento(id_magento):
    """
    Recebe um id Magento e retorna o Id Nuvemshop correspondente, ou ""
    """
    id_magento = str(id_magento)

    with open(_JSON_PATH, "r", encoding="utf-8") as f:
        categorias = json.load(f)

    def buscar(cat):
        if cat.get("id_magento") == id_magento:
            return cat.get("id_nuvemshop", "")

        for filho in cat.get("children", []):
            achado = buscar(filho)
            if achado:
                return achado

        return ""

    for raiz in categorias:
        resultado = buscar(raiz)
        if resultado:
            return resultado

    return ""
