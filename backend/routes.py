from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Task, TaskCreate, TaskRead, TaskUpdate
from db import SessionDep

tasks = APIRouter(prefix="/tasks", tags=["Tareas"])

@tasks.post("/", response_model=TaskRead)
def crear_tarea(tarea: TaskCreate, session: SessionDep): # type: ignore
    item = Task.from_orm(tarea)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item 

@tasks.get("/", response_model=list[TaskRead])
def obtener_tareas(session: SessionDep): #  type: ignore
    return session.exec(select(Task)).all()


@tasks.get("/{tarea_id}", response_model=TaskRead)
def obtener_tarea(tarea_id: int, session: SessionDep): # type: ignore
    tarea = session.get(Task, tarea_id)
    
    if not tarea:
        raise HTTPException(status_code=404, detail="No existe esta tarea")
    
    return tarea

@tasks.put("/{tarea_id}", response_model=TaskRead)
def actualizar_tarea(tarea_id: int, campo: TaskUpdate, session: SessionDep): # type: ignore
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

@tasks.delete("/{tarea_id}")
def borrar_tarea(tarea_id : int, session: SessionDep): # type: ignore
    tarea = session.get(Task, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="No existe esta tarea")
    
    session.delete(tarea)
    session.commit()
    return {"Message" : "Tarea eliminada existosamente"}
