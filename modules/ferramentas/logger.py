import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


FULL_PATH = os.path.join(BASE_DIR, '.logs/migracao')


def novo_log(mensagem: str, base_dir, sku=""):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    pasta = os.path.join(FULL_PATH, base_dir)
    os.makedirs(pasta, exist_ok=True)

    arquivo = os.path.join(pasta, f"{sku}.txt")
    with open(arquivo, "a", encoding="utf-8") as f:
        f.write(f"\n----------------------------------------------------------------------------\ntimestamp:{timestamp}\n\n{mensagem}\n")