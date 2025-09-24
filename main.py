from fastapi import Depends, FastAPI
from typing import Annotated
from sqlmodel import SQLModel, Session, create_engine


app = FastAPI()


rds_connection_string = "postgresql://postgres:postgres@database-1.cubwsk6oid9n.us-east-1.rds.amazonaws.com:5432/test"
engine = create_engine(rds_connection_string, echo=True)


@app.get("/health")
def health_check():
    try:
        with Session(engine) as session:
            result = session.exec(text("SELECT 1")).first()
        return {"status": "ok", "db_response": result}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


