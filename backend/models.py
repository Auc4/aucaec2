from typing import Optional
from sqlmodel import SQLModel, Field

class TaskBase(SQLModel):
    title : str = Field(max_length=200)
    description : Optional[str] = Field(default=None, max_length=500)
    completed : bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
