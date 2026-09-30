from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import Base, engine, get_db
from . import models, schemas
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


@app.get("/api/inventario", response_model=List[schemas.ProdutoResponse])
def inventario(db: Session = Depends(get_db)):
    return db.query(models.Produto).all()