from fastapi import FastAPI
from db import create_all_tables
from routes import tasks

app = FastAPI(lifespan=create_all_tables)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # acepta todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],      # acepta todos los métodos (GET, POST, PUT, DELETE, etc)
    allow_headers=["*"],      # acepta todos los headers
)

app.include_router(tasks)
