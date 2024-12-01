from sqlmodel import SQLModel, Column, Field, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
from typing import Optional, List


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    # Relationship
    rsvps: Optional[List["RSVP"]] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Event(SQLModel, table=True):
    __tablename__ = "events"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    creator: str
    description: str
    location: str
    category: str
    capacity: int
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    rsvps: Optional[List["RSVP"]] = Relationship(
        back_populates="event", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self) -> str:
        return f"<Event {self.title}>"

    def rsvp_count(self) -> int:
        return len(self.rsvps)


class RSVP(SQLModel, table=True):
    __tablename__ = "rsvps"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    user_uid: uuid.UUID = Field(nullable=False, foreign_key="users.uid")
    event_uid: uuid.UUID = Field(nullable=False, foreign_key="events.uid")
    rsvp_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    # Use forward reference to avoid issues with model initialization order
    event: Optional["Event"] = Relationship(back_populates="rsvps")
    user: Optional["User"] = Relationship(back_populates="rsvps")

    def __repr__(self) -> str:
        return f"<RSVP user_uid={self.user_uid}, event_uid={self.event_uid}>"
