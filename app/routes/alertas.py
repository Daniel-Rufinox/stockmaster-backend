from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta

from ..database import get_db
from .. import models

router = APIRouter(
    prefix="/api/alertas",
    tags=["Alertas"]
)


@router.get("/estoque-minimo")
def alerta_estoque_minimo(
    db: Session = Depends(get_db)
):
    produtos = db.query(models.Produto).filter(
        models.Produto.quantidade <= models.Produto.minimo
    ).all()

    return [
        {
            "id": produto.id,
            "codigo": produto.codigo,
            "nome": produto.nome,
            "quantidade": produto.quantidade,
            "minimo": produto.minimo,
            "situacao": "Estoque crítico"
        }
        for produto in produtos
    ]


@router.get("/validade")
def alerta_validade(
    db: Session = Depends(get_db)
):
    hoje = date.today()
    limite = hoje + timedelta(days=30)

    produtos = db.query(models.Produto).filter(
        models.Produto.validade.isnot(None),
        models.Produto.validade <= limite
    ).all()

    resultado = []

    for produto in produtos:
        if produto.validade < hoje:
            situacao = "Vencido"
        else:
            situacao = "Próximo do vencimento"

        resultado.append(
            {
                "id": produto.id,
                "codigo": produto.codigo,
                "nome": produto.nome,
                "validade": produto.validade,
                "situacao": situacao
            }
        )

    return resultado