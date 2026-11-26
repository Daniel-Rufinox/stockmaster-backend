
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/api/fornecedores",
    tags=["Fornecedores"]
)


@router.post(
    "/",
    response_model=schemas.FornecedorResponse,
    status_code=201
)
def criar_fornecedor(
    dados: schemas.FornecedorCreate,
    db: Session = Depends(get_db)
):
    if dados.cnpj:
        existente = db.query(models.Fornecedor).filter(
            models.Fornecedor.cnpj == dados.cnpj
        ).first()

        if existente:
            raise HTTPException(
                status_code=400,
                detail="Este CNPJ já está cadastrado."
            )

    fornecedor = models.Fornecedor(**dados.model_dump())

    db.add(fornecedor)
    db.commit()
    db.refresh(fornecedor)

    return fornecedor


@router.get(
    "/",
    response_model=List[schemas.FornecedorResponse]
)
def listar_fornecedores(
    db: Session = Depends(get_db)
):
    return db.query(models.Fornecedor).order_by(
        models.Fornecedor.nome
    ).all()


@router.get(
    "/{fornecedor_id}",
    response_model=schemas.FornecedorResponse
)
def buscar_fornecedor(
    fornecedor_id: int,
    db: Session = Depends(get_db)
):
    fornecedor = db.query(models.Fornecedor).filter(
        models.Fornecedor.id == fornecedor_id
    ).first()

    if not fornecedor:
        raise HTTPException(
            status_code=404,
            detail="Fornecedor não encontrado."
        )

    return fornecedor


@router.put(
    "/{fornecedor_id}",
    response_model=schemas.FornecedorResponse
)
def atualizar_fornecedor(
    fornecedor_id: int,
    dados: schemas.FornecedorUpdate,
    db: Session = Depends(get_db)
):
    fornecedor = db.query(models.Fornecedor).filter(
        models.Fornecedor.id == fornecedor_id
    ).first()

    if not fornecedor:
        raise HTTPException(
            status_code=404,
            detail="Fornecedor não encontrado."
        )

    atualizados = dados.model_dump(exclude_unset=True)

    if atualizados.get("cnpj"):
        duplicado = db.query(models.Fornecedor).filter(
            models.Fornecedor.cnpj == atualizados["cnpj"],
            models.Fornecedor.id != fornecedor_id
        ).first()

        if duplicado:
            raise HTTPException(
                status_code=400,
                detail="Este CNPJ já pertence a outro fornecedor."
            )

    for campo, valor in atualizados.items():
        setattr(fornecedor, campo, valor)

    db.commit()
    db.refresh(fornecedor)

    return fornecedor


@router.delete("/{fornecedor_id}")
def excluir_fornecedor(
    fornecedor_id: int,
    db: Session = Depends(get_db)
):
    fornecedor = db.query(models.Fornecedor).filter(
        models.Fornecedor.id == fornecedor_id
    ).first()

    if not fornecedor:
        raise HTTPException(
            status_code=404,
            detail="Fornecedor não encontrado."
        )

    db.delete(fornecedor)
    db.commit()

    return {
        "message": "Fornecedor excluído com sucesso."
    }
