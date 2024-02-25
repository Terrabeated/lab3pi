from pydantic import BaseModel
from datetime import date

class BaseEvent(BaseModel):
    date: date
    title: str
    description: str
    type: str

class Event(BaseEvent):
    id: int

class EventPreview(BaseModel):
    id: int
    type: str
    description: str