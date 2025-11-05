import re
from html import unescape

def remover_html_do_texto(texto):
    """
    Recebe uma str com HTML e retorna a str sem as tags HTML.
    """
    if not isinstance(texto, str):
        return texto
    texto = re.sub(r'<(script|style).*?>.*?</\1>', '', texto, flags=re.DOTALL | re.IGNORECASE)
    texto = re.sub(r'<br\s*/?>', '\n', texto, flags=re.IGNORECASE)
    texto = re.sub(r'</p\s*>', '\n\n', texto, flags=re.IGNORECASE)
    texto = re.sub(r'<p\s*>', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = unescape(texto)
    linhas = [linha.strip().replace('\n', ' ') for linha in texto.split('\n\n')]
    texto_limpo = '\n\n'.join(linhas).strip()
    texto_limpo = re.sub(r'\n{3,}', '\n\n', texto_limpo)
    return texto_limpo