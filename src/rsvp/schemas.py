from pydantic import BaseModel
import uuid
from datetime import datetime


class RSVP(BaseModel):
    uid: uuid.UUID
    event_uid: uuid.UUID
    user_uid: uuid.UUID
    rsvp_date: datetime


class RSVPCreateModel(BaseModel):
    event_uid: uuid.UUID
