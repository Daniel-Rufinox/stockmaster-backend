
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from .database import Base, engine, get_db, SessionLocal
from . import models, schemas
from .routes import (
    produtos,
    movimentacoes,
    alertas,
    usuarios,
    fornecedores,
    categorias
)


# Cria as tabelas que ainda não existem
Base.metadata.create_all(bind=engine)


# Importa as categorias já utilizadas pelos produtos
# para a nova tabela de categorias.
def sincronizar_categorias_existentes():
    db = SessionLocal()

    try:
        nomes = db.query(
            models.Produto.categoria
        ).distinct().all()

        for item in nomes:
            nome = item[0]

            if not nome or not nome.strip():
                continue

            nome = nome.strip()

            existente = db.query(models.Categoria).filter(
                func.lower(models.Categoria.nome) == nome.lower()
            ).first()

            if not existente:
                db.add(models.Categoria(nome=nome))

        db.commit()

    finally:
        db.close()


sincronizar_categorias_existentes()


app = FastAPI(
    title="StockMaster API",
    description="API Back-End do sistema StockMaster para gerenciamento e controle de estoque.",
    version="1.1.0"
)


# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registro das rotas
app.include_router(produtos.router)
app.include_router(movimentacoes.router)
app.include_router(alertas.router)
app.include_router(usuarios.router)
app.include_router(fornecedores.router)
app.include_router(categorias.router)


@app.get("/")
def root():
    return {
        "message": "StockMaster API está funcionando!"
    }


@app.get(
    "/api/inventario",
    response_model=List[schemas.ProdutoResponse]
)
def inventario(db: Session = Depends(get_db)):
    return db.query(models.Produto).all()
