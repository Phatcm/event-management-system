from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import List
from .schemas import Event, EventCreateModel, EventUpdateModel
from .service import EventService
from src.db.main import get_session

event_router = APIRouter()
event_service = EventService()


@event_router.get("/", response_model=List[Event])
async def get_all_events(session: AsyncSession = Depends(get_session)):
    events = await event_service.get_all_events(session)
    return events


@event_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Event)
async def create_an_event(
    event_data: EventCreateModel, session: AsyncSession = Depends(get_session)
) -> dict:
    new_event = await event_service.create_event(event_data, session)
    return new_event


@event_router.get("/{event_uid}", response_model=Event)
async def get_an_event(
    event_uid: str, session: AsyncSession = Depends(get_session)
) -> dict:
    event = await event_service.get_event(event_uid, session)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return event


@event_router.patch("/{event_uid}", response_model=Event)
async def update_an_event(
    event_uid: str,
    book_update_data: EventUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_book = await event_service.update_event(
        event_uid, book_update_data, session
    )
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return updated_book


@event_router.delete("/{event_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_event(event_uid: str, session: AsyncSession = Depends(get_session)):
    book_to_delete = await event_service.delete_event(event_uid, session)
    if not book_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return None
