from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class User(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserCreateModel(BaseModel):
    username: str = Field(..., min_length=6, max_length=16)
    email: str = Field(..., max_length=40)
    password: str = Field(..., min_length=6, max_length=16)
    first_name: str = Field(..., max_length=25)
    last_name: str = Field(..., max_length=25)


class UserLoginModel(BaseModel):
    email: str = Field(..., max_length=40)
    password: str = Field(..., min_length=6, max_length=16)
