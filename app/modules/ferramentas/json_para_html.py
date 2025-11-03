
def json_para_html(produto):
    html = f"""
<html>
<head>
    <meta charset="UTF-8">
    <title>{produto.get('nome', '')}</title>
    <meta name="description" content="{produto.get('metadescricao', '')}">
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 16px;
            color: #000;
            margin: 40px;
            line-height: 1.5;
        }}
        h1, h2, p, li, th, td {{
            font-weight: normal;
            font-size: 16px;
            margin: 10px 0;
        }}
        ul {{
            margin-left: 20px;
            padding-left: 0;
        }}
        table {{
            border-collapse: collapse;
            margin-top: 10px;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #000;
            padding: 6px;
            text-align: left;
        }}
    </style>
</head>
<body>
    <h1>{produto.get('nome', '')}</h1>
    <h2>Marca: {produto.get('marca', '')}</h2>
    <p>{produto.get('descricao', '')}</p>
"""

    # Escopos (lista)
    if 'Escopos' in produto and isinstance(produto['Escopos'], list):
        html += "<h2>Escopos de uso:</h2>\n<ul>\n"
        for item in produto['Escopos']:
            html += f"    <li>{item.lstrip('- ').strip()}</li>\n"
        html += "</ul>\n"

    # Ficha Técnica (dicionário)
    if 'Ficha Técnica' in produto and isinstance(produto['Ficha Técnica'], dict):
        html += "<h2>Ficha Técnica:</h2>\n<table>\n"
        for chave, valor in produto['Ficha Técnica'].items():
            html += f"    <tr><th>{chave}</th><td>{valor}</td></tr>\n"
        html += "</table>\n"

    # Mais sobre o produto (texto adicional)
    if 'Mais sobre o produto' in produto:
        html += f"<h2>Mais sobre o produto:</h2>\n<p>{produto['Mais sobre o produto']}</p>\n"

    html += "</body>\n</html>"
    return html