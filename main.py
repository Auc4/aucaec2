from fastapi import Depends, FastAPI
from db import create_all_tables
from routes import users


app = FastAPI(lifespan=create_all_tables)

app.include_router(users)


