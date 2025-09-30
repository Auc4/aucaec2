from fastapi import FastAPI
from db import create_all_tables
from routes import tasks

app = FastAPI(lifespan=create_all_tables)
app.include_router(tasks)