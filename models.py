from typing import Optional
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title : str = Field(max_lenght=200)
    description : Optional[str] = Field(default=None, max_length=500)
    completed : bool = Field(default=False)

    