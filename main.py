from fastapi import FastAPI
from sqlmodel import SQLModel, Field
from typing import Optional

app = FastAPI()

usuarios = []

class Usuario(SQLModel):
    id: Optional[int] = Field(default=None)
    nombre: str
    email: str

class ActualizarUsuario(SQLModel):
    nombre: Optional[str] = None
    email: Optional[str] = None

@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    usuario.id = len(usuarios) + 1
    usuarios.append(usuario)
    return usuario

@app.get("/usuarios")
def obtener_usuario():
    return usuarios

@app.delete("/usuarios/{id}")
def eliminar_usuario(id: int):
    for index, usuario in enumerate(usuarios):
        if usuario.id == id:
            usuarios.pop(index)
            return "Usuario Eliminado"
        
@app.patch("/usuarios/{id}")
def actualizar_usuario(id:int , usuario_nuevo : ActualizarUsuario):
    for usuario in usuarios:
        if usuario.id == id:
            if usuario_nuevo.nombre is not None:
                usuario.nombre = usuario_nuevo.nombre 
            if usuario_nuevo.email is not None:
                usuario.email = usuario_nuevo.email
            return usuario