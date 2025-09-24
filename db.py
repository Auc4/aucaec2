from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session
from sqlmodel import create_engine

rds_connection_string = "postgresql://postgres:postgres@database-1.cubwsk6oid9n.us-east-1.rds.amazonaws.com:5432/test"
engine = create_engine(rds_connection_string, echo=True)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated(Session, Depends(get_session))