from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/api/movimentacoes",
    tags=["Movimentações"]
)


@router.post(
    "/entrada",
    response_model=schemas.MovimentacaoResponse,
    status_code=201
)
def registrar_entrada(
    dados: schemas.EntradaEstoque,
    db: Session = Depends(get_db)
):
    if dados.quantidade <= 0:
        raise HTTPException(
            status_code=400,
            detail="A quantidade deve ser maior que zero."
        )

    produto = db.query(models.Produto).filter(
        models.Produto.id == dados.produto_id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    produto.quantidade += dados.quantidade

    if dados.fornecedor is not None:
        produto.fornecedor = dados.fornecedor

    if dados.validade is not None:
        produto.validade = dados.validade

    movimentacao = models.Movimentacao(
        produto_id=produto.id,
        tipo="entrada",
        quantidade=dados.quantidade,
        motivo="Compra",
        observacao=dados.observacao
    )

    db.add(movimentacao)
    db.commit()
    db.refresh(movimentacao)

    return movimentacao


@router.post(
    "/saida",
    response_model=schemas.MovimentacaoResponse,
    status_code=201
)
def registrar_saida(
    dados: schemas.SaidaEstoque,
    db: Session = Depends(get_db)
):
    if dados.quantidade <= 0:
        raise HTTPException(
            status_code=400,
            detail="A quantidade deve ser maior que zero."
        )

    motivos_permitidos = ["Venda", "Perda", "Descarte"]

    if dados.motivo not in motivos_permitidos:
        raise HTTPException(
            status_code=400,
            detail="Motivo deve ser Venda, Perda ou Descarte."
        )

    produto = db.query(models.Produto).filter(
        models.Produto.id == dados.produto_id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    if dados.quantidade > produto.quantidade:
        raise HTTPException(
            status_code=400,
            detail="Estoque insuficiente para realizar a saída."
        )

    produto.quantidade -= dados.quantidade

    movimentacao = models.Movimentacao(
        produto_id=produto.id,
        tipo="saida",
        quantidade=dados.quantidade,
        motivo=dados.motivo,
        observacao=dados.observacao
    )

    db.add(movimentacao)
    db.commit()
    db.refresh(movimentacao)

    return movimentacao


@router.get(
    "/",
    response_model=List[schemas.MovimentacaoResponse]
)
def listar_movimentacoes(
    db: Session = Depends(get_db)
):
    return db.query(models.Movimentacao).order_by(
        models.Movimentacao.data.desc()
    ).all()