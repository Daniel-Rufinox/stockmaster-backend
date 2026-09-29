from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    quantidade = Column(Integer, default=0)
    minimo = Column(Integer, default=0)
    preco = Column(Float, default=0)
    fornecedor = Column(String, nullable=True)
    validade = Column(Date, nullable=True)

    movimentacoes = relationship(
        "Movimentacao",
        back_populates="produto",
        cascade="all, delete-orphan"
    )


class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False
    )
    tipo = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    motivo = Column(String, nullable=True)
    observacao = Column(String, nullable=True)
    data = Column(DateTime, default=datetime.utcnow)

    produto = relationship(
        "Produto",
        back_populates="movimentacoes"
    )


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    usuario = Column(String, unique=True, nullable=False, index=True)
    senha = Column(String, nullable=False)
    perfil = Column(String, nullable=False, default="Operador")