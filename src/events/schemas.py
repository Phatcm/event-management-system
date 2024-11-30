import uuid
from typing import Optional, Dict, List
from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
    uid: uuid.UUID
    title: str
    creator: str
    description: str
    location: str
    category: str
    capacity: int
    created_at: datetime
    updated_at: datetime


class EventCreateModel(BaseModel):
    title: str
    creator: str
    description: str
    location: str
    category: str
    capacity: int


class EventUpdateModel(BaseModel):
    title: str
    creator: str
    description: str
    location: str
    category: str
    capacity: int
