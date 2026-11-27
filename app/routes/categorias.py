
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/api/categorias",
    tags=["Categorias"]
)


@router.post(
    "/",
    response_model=schemas.CategoriaResponse,
    status_code=201
)
def criar_categoria(
    dados: schemas.CategoriaCreate,
    db: Session = Depends(get_db)
):
    nome = dados.nome.strip()

    if not nome:
        raise HTTPException(
            status_code=400,
            detail="O nome da categoria é obrigatório."
        )

    existente = db.query(models.Categoria).filter(
        func.lower(models.Categoria.nome) == nome.lower()
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="Esta categoria já está cadastrada."
        )

    categoria = models.Categoria(nome=nome)

    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    return categoria


@router.get(
    "/",
    response_model=List[schemas.CategoriaResponse]
)
def listar_categorias(
    db: Session = Depends(get_db)
):
    return db.query(models.Categoria).order_by(
        models.Categoria.nome
    ).all()


@router.get(
    "/{categoria_id}",
    response_model=schemas.CategoriaResponse
)
def buscar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    categoria = db.query(models.Categoria).filter(
        models.Categoria.id == categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada."
        )

    return categoria


@router.put(
    "/{categoria_id}",
    response_model=schemas.CategoriaResponse
)
def atualizar_categoria(
    categoria_id: int,
    dados: schemas.CategoriaUpdate,
    db: Session = Depends(get_db)
):
    categoria = db.query(models.Categoria).filter(
        models.Categoria.id == categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada."
        )

    atualizados = dados.model_dump(exclude_unset=True)

    if "nome" in atualizados:
        nome = atualizados["nome"]

        if nome is None or not nome.strip():
            raise HTTPException(
                status_code=400,
                detail="O nome da categoria é obrigatório."
            )

        nome = nome.strip()

        duplicada = db.query(models.Categoria).filter(
            func.lower(models.Categoria.nome) == nome.lower(),
            models.Categoria.id != categoria_id
        ).first()

        if duplicada:
            raise HTTPException(
                status_code=400,
                detail="Já existe uma categoria com esse nome."
            )

        nome_antigo = categoria.nome

        # Atualiza também os produtos que usam essa categoria.
        db.query(models.Produto).filter(
            func.lower(models.Produto.categoria) == nome_antigo.lower()
        ).update(
            {"categoria": nome},
            synchronize_session=False
        )

        categoria.nome = nome

    db.commit()
    db.refresh(categoria)

    return categoria


@router.delete("/{categoria_id}")
def excluir_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    categoria = db.query(models.Categoria).filter(
        models.Categoria.id == categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada."
        )

    em_uso = db.query(models.Produto).filter(
        func.lower(models.Produto.categoria) == categoria.nome.lower()
    ).first()

    if em_uso:
        raise HTTPException(
            status_code=400,
            detail="Não é possível excluir: existem produtos usando esta categoria."
        )

    db.delete(categoria)
    db.commit()

    return {
        "message": "Categoria excluída com sucesso."
    }
