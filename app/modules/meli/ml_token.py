import requests
from config import settings

# 🔹 ID do arquivo JSON no Drive
FILE_ID = settings.MELI_API_KEY
URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

def get_meli_token():
    response = requests.get(URL)
    response.raise_for_status()  # lança erro se falhar
    tokens = response.json()
    return tokens["access_token"]