from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db import SessionDep
from models import Usuario

users = APIRouter(prefix="/usuarios", tags=["usuarios"])


@users.post("/", response_model=Usuario)
def crear_usuario(usuario: Usuario, session: SessionDep):
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@users.get("/", response_model=list[Usuario])
def listar_usuarios(session: SessionDep):
    return session.exec(select(Usuario)).all()


@users.get("/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@users.put("/{usuario_id}", response_model=Usuario)
def actualizar_usuario(usuario_id: int, datos: Usuario, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = datos.nombre
    usuario.email = datos.email

    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@users.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    session.delete(usuario)
    session.commit()
    return {"ok": True}
