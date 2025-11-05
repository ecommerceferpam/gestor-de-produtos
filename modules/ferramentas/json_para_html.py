
def json_para_html(produto):
    html = f"""
    <p><strong>{produto.get('nome', '')}</p></strong>
    <p>{produto.get('marca', '')}</p>
    <p> <br></p>
    <p>{produto.get('descricao', '')}</p>
    <p> <br></p>
"""

    # Escopos (lista)
    if 'escopos' in produto and isinstance(produto['escopos'], list):
        for item in produto['escopos']:
            html += f"    <p>- {item}</p>\n"
        html += "<p> <br></p>"

    # Ficha Técnica (dicionário)
    if 'ficha_tecnica' in produto and isinstance(produto['ficha_tecnica'], dict):
        html += "<p><strong>Ficha Técnica:</p></strong>\n<table border='1'><tbody>\n"
        for chave, valor in produto['ficha_tecnica'].items():
            html += f"    <tr><td><p>{chave}</p></td><td><p>{valor}</p></td></tr>\n"
        html += "</tbody></table>\n<p> <br></p>"

    # Sugestões de Uso  (lista)
    if 'sugestoes_de_uso' in produto and isinstance(produto['sugestoes_de_uso'], list):
        html += "<p><strong>Sugestões de Uso:</p></strong>"
        for item in produto['sugestoes_de_uso']:
            html += f"    <p>- {item}</p>\n"
        html += "<p> <br></p>"

    # Mais sobre o produto (texto adicional)
    if 'mais_sobre_o_produto' in produto:
        html += f"<p><strong>Mais sobre o produto:</p></strong>\n<p>{produto['mais_sobre_o_produto']}</p>\n"

    return html