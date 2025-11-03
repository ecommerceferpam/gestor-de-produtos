from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import importlib
import inspect
import pkgutil
from typing import Any, Dict
from app.auth import verify_api_key
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Auto-Exposed Modules API")

# depois de app = FastAPI(...)
origins = [
    "http://localhost:5500",   # porta onde você abre o HTML (ajuste se usar outra)
    "http://127.0.0.1:5500",
    "http://localhost:3000",   # outras origens de teste
    "http://127.0.0.1:3000",
    "http://localhost:8000",   # opcional: permitir chamadas do próprio backend
    "*",                       # só deixar '*' se for só em dev; preferível listar origens
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # ou ["*"] em dev
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["*"],              # ou ["content-type","x-api-key"] para mais segurança
)

# carregar dinamicamente todos os módulos em app.modules
import app.modules as modules_pkg

def load_module_names():
    return [name for _, name, _ in pkgutil.iter_modules(modules_pkg.__path__)]

def make_endpoint(module_name: str, func):
    async def endpoint(body: Dict[str, Any], api_key: str = Depends(verify_api_key)):
        """
        Recebe JSON com argumentos por nome (kwargs).
        Exemplo body: {"product_id": 1} ou {"lista": [...], "chave":"id", "valor":1}
        """
        if not isinstance(body, dict):
            raise HTTPException(status_code=400, detail="Body must be a JSON object with kwargs.")
        sig = inspect.signature(func)
        try:
            # permitir passar apenas os parâmetros que a função espera
            filtered_kwargs = {k: v for k, v in body.items() if k in sig.parameters}
            result = func(**filtered_kwargs)
            return JSONResponse(content={"success": True, "result": result})
        except TypeError as e:
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return endpoint

# criar rotas dinamicamente: /{module}/{function}
for module_name in load_module_names():
    module = importlib.import_module(f"app.modules.{module_name}")
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if name.startswith("_"):
            continue
        route_path = f"/{module_name}/{name}"
        endpoint = make_endpoint(module_name, obj)
        # registra como POST
        app.post(route_path)(endpoint)

@app.get("/")
def root():
    return {"msg": "API up. Veja /docs para ver rotas."}