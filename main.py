from fastapi import Depends, FastAPI
from sqlmodel import select
from db import create_all_tables, SessionDep


app = FastAPI(lifespan=create_all_tables)

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get("/check-db")
def check_db(session: SessionDep):
    result = session.exec(select()).first()
    return {"db_status": result}


