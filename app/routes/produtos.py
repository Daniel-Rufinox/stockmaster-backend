from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/api/produtos",
    tags=["Produtos"]
)


@router.post("/", response_model=schemas.ProdutoResponse, status_code=201)
def criar_produto(
    produto: schemas.ProdutoCreate,
    db: Session = Depends(get_db)
):
    produto_existente = db.query(models.Produto).filter(
        models.Produto.codigo == produto.codigo
    ).first()

    if produto_existente:
        raise HTTPException(
            status_code=400,
            detail="Já existe um produto com este código."
        )

    novo_produto = models.Produto(**produto.model_dump())

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@router.get("/", response_model=List[schemas.ProdutoResponse])
def listar_produtos(
    busca: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Produto)

    if busca:
        query = query.filter(
            (models.Produto.nome.ilike(f"%{busca}%")) |
            (models.Produto.codigo.ilike(f"%{busca}%"))
        )

    return query.all()


@router.get("/{produto_id}", response_model=schemas.ProdutoResponse)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):
    produto = db.query(models.Produto).filter(
        models.Produto.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    return produto


@router.put("/{produto_id}", response_model=schemas.ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    dados: schemas.ProdutoUpdate,
    db: Session = Depends(get_db)
):
    produto = db.query(models.Produto).filter(
        models.Produto.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    dados_atualizados = dados.model_dump(exclude_unset=True)

    if "codigo" in dados_atualizados:
        codigo_existente = db.query(models.Produto).filter(
            models.Produto.codigo == dados_atualizados["codigo"],
            models.Produto.id != produto_id
        ).first()

        if codigo_existente:
            raise HTTPException(
                status_code=400,
                detail="Já existe outro produto com este código."
            )

    for campo, valor in dados_atualizados.items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    return produto


@router.delete("/{produto_id}")
def excluir_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):
    produto = db.query(models.Produto).filter(
        models.Produto.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    db.delete(produto)
    db.commit()

    return {
        "message": "Produto excluído com sucesso."
    }