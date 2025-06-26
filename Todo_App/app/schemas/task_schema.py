from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    due_date: datetime
    
# Inheriting name and due_date
class TaskCreate(TaskBase):
    pass  

class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    due_date: Optional[datetime]
    completed: Optional[bool]

class TaskOut(TaskBase):
    id: str
    created_at: datetime
    completed: bool
    owner: str
