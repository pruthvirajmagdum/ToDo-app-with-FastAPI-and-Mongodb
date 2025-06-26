from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo


IST = ZoneInfo("Asia/Kolkata")

class TaskCreate(BaseModel):
    name: str
    due_date: Optional[datetime] = Field(default_factory=lambda: datetime.now(IST))

    @validator("name", pre=True)
    def title_not_blank(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty or just spaces")
        return v.strip()

    @validator("due_date")
    def due_date_must_be_future(cls, value):
        ist_now = datetime.now(ZoneInfo("Asia/Kolkata"))
        if value < ist_now:
            raise ValueError("Due date must be in the future (IST)")
        return value



class Taskcreate(TaskCreate):
    pass

class TaskInDB(TaskCreate):
    id: str
    created_at: datetime
    completed: bool = False
    owner: str
