from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional


# =========================
# PRODUTOS
# =========================

class ProdutoBase(BaseModel):
    codigo: str
    nome: str
    categoria: str
    quantidade: int = 0
    minimo: int = 0
    preco: float = 0
    fornecedor: Optional[str] = None
    validade: Optional[date] = None


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    codigo: Optional[str] = None
    nome: Optional[str] = None
    categoria: Optional[str] = None
    quantidade: Optional[int] = None
    minimo: Optional[int] = None
    preco: Optional[float] = None
    fornecedor: Optional[str] = None
    validade: Optional[date] = None


class ProdutoResponse(ProdutoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# MOVIMENTAÇÕES
# =========================

class EntradaEstoque(BaseModel):
    produto_id: int
    quantidade: int
    fornecedor: Optional[str] = None
    validade: Optional[date] = None
    observacao: Optional[str] = None


class SaidaEstoque(BaseModel):
    produto_id: int
    quantidade: int
    motivo: str
    observacao: Optional[str] = None


class MovimentacaoResponse(BaseModel):
    id: int
    produto_id: int
    tipo: str
    quantidade: int
    motivo: Optional[str] = None
    observacao: Optional[str] = None
    data: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================
# USUÁRIOS
# =========================

class UsuarioCreate(BaseModel):
    nome: str
    usuario: str
    senha: str
    perfil: str = "Operador"


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    usuario: Optional[str] = None
    senha: Optional[str] = None
    perfil: Optional[str] = None


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    usuario: str
    perfil: str

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    usuario: str
    senha: str