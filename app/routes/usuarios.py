from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/api/usuarios",
    tags=["Usuários"]
)


@router.post("/", response_model=schemas.UsuarioResponse, status_code=201)
def criar_usuario(
    dados: schemas.UsuarioCreate,
    db: Session = Depends(get_db)
):
    usuario_existente = db.query(models.Usuario).filter(
        models.Usuario.usuario == dados.usuario
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Este nome de usuário já está cadastrado."
        )

    if dados.perfil not in ["Administrador", "Operador"]:
        raise HTTPException(
            status_code=400,
            detail="Perfil deve ser Administrador ou Operador."
        )

    novo_usuario = models.Usuario(
        nome=dados.nome,
        usuario=dados.usuario,
        senha=dados.senha,
        perfil=dados.perfil
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


@router.get("/", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db)
):
    return db.query(models.Usuario).all()


@router.put("/{usuario_id}", response_model=schemas.UsuarioResponse)
def atualizar_usuario(
    usuario_id: int,
    dados: schemas.UsuarioUpdate,
    db: Session = Depends(get_db)
):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    dados_atualizados = dados.model_dump(exclude_unset=True)

    if "perfil" in dados_atualizados:
        if dados_atualizados["perfil"] not in ["Administrador", "Operador"]:
            raise HTTPException(
                status_code=400,
                detail="Perfil deve ser Administrador ou Operador."
            )

    if "usuario" in dados_atualizados:
        duplicado = db.query(models.Usuario).filter(
            models.Usuario.usuario == dados_atualizados["usuario"],
            models.Usuario.id != usuario_id
        ).first()

        if duplicado:
            raise HTTPException(
                status_code=400,
                detail="Este nome de usuário já está cadastrado."
            )

    for campo, valor in dados_atualizados.items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)

    return usuario


@router.delete("/{usuario_id}")
def excluir_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    db.delete(usuario)
    db.commit()

    return {"message": "Usuário excluído com sucesso."}


@router.post("/login")
def login(
    dados: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.usuario == dados.usuario,
        models.Usuario.senha == dados.senha
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos."
        )

    return {
        "message": "Login realizado com sucesso.",
        "id": usuario.id,
        "nome": usuario.nome,
        "usuario": usuario.usuario,
        "perfil": usuario.perfil
    }