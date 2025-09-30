from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db import SessionDep
from models import Task

tasks = APIRouter(prefix="/tasks", tags=["Tareas"])

@tasks.post("/", responde_model=Task)
def crear_tarea(tarea: Task, session: SessionDep): # type: ignore
    session.add(tarea)
    session.commit()
    session.refresh(tarea)
    return tarea

@tasks.get("/", response_model=list[Task])
def obtener_tareas(session: SessionDep): #  type: ignore
    session.exec(select(Task)).all()


@tasks.get("/{tarea_id}", response_model=Task)
def obtener_tarea(tarea_id: int, session: SessionDep): # type: ignore
    tarea = session.get(Task, tarea_id)
    
    if not tarea:
        raise HTTPException(status_code=404, detail="No existe esta tarea")
    
    return tarea

@tasks.put("/{tarea_id}", response_model=Task)
def actualizar_tarea(tarea_id: int, campo: Task, session: SessionDep): # type: ignore
    tarea = session.get(Task, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="No existe esta tarea")

    tarea.title = campo.title
    tarea.description = campo.description
    tarea.completed = campo.completed

    session.add(tarea)
    session.commit()
    session.refresh(tarea)
    return tarea

@tasks.delete("/{tarea_id}", response_model=Task)
def borrar_tarea(tarea_id : int, session: SessionDep): # type: ignore
    tarea = session.get(Task, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="No existe esta tarea")
    
    session.delete(tarea)
    session.commit()
    return {"Message" : "Tarea eliminada existosamente"}