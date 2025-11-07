def padronizar_sku(value: str | int) -> str:
    """
    Formata o valor para 7 dígitos, preenchendo com zeros à esquerda.

    Exemplos:
        pad7("123") -> "0000123"
        pad7(45)    -> "0000045"
    """
    return str(value).zfill(7)
