import uuid
from typing import Optional, Dict, List
from src.rsvp.schemas import RSVP
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
    rsvps: List[RSVP]


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
