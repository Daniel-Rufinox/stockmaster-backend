from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from . import models
from .routes import produtos, movimentacoes, alertas, usuarios


# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="StockMaster API",
    description="API Back-End do sistema StockMaster para gerenciamento e controle de estoque.",
    version="1.0.0"
)


# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rotas
app.include_router(produtos.router)
app.include_router(movimentacoes.router)
app.include_router(alertas.router)
app.include_router(usuarios.router)


@app.get("/")
def root():
    return {
        "message": "StockMaster API está funcionando!"
    }


@app.get("/api/inventario")
def inventario():
    return {
        "message": "Utilize /api/produtos para consultar o inventário."
    }