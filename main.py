from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import users
from app.router import fincas
from app.router import auth
from app.router import produccion_huevos
from app.router import stock
from app.router import tipo_huevos  #

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/access", tags=["login"])
app.include_router(fincas.router, prefix="/fincas", tags=["fincas"])
app.include_router(produccion_huevos.router, prefix="/produccion-huevos", tags=["produccion-huevos"])
app.include_router(stock.router, prefix="/stock", tags=["stock"])
app.include_router(tipo_huevos.router, prefix="/tipo-huevos", tags=["tipo-huevos"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "ok",
        "autor": "ADSO 2925889"
    }
