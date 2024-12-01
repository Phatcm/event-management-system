from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import List
from .schemas import Event, EventCreateModel, EventUpdateModel
from .service import EventService
from src.db.main import get_session
from src.auth.depends import AccessTokenBearer, RoleChecker

event_router = APIRouter()
event_service = EventService()
access_token_bearer = AccessTokenBearer()
# role_checker = Depends(RoleChecker(["admin", "organizer", "user"]))


@event_router.get(
    "/",
    response_model=List[Event],
    dependencies=[Depends(RoleChecker(["admin", "organizer", "user"]))],
)
async def get_all_events(
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access_token_bearer),
):
    events = await event_service.get_all_events(session)
    return events


@event_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Event,
    dependencies=[Depends(RoleChecker(["admin", "organizer"]))],
)
async def create_an_event(
    event_data: EventCreateModel,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access_token_bearer),
) -> dict:
    user_uid = token_detail.get("user")["user_uid"]
    new_event = await event_service.create_event(event_data, user_uid, session)
    return new_event


@event_router.get(
    "/{event_uid}",
    response_model=Event,
    dependencies=[Depends(RoleChecker(["admin", "organizer"]))],
)
async def get_an_event(
    event_uid: str,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access_token_bearer),
) -> dict:
    event = await event_service.get_event(event_uid, session)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return event


@event_router.patch(
    "/{event_uid}",
    response_model=Event,
    dependencies=[Depends(RoleChecker(["admin", "organizer"]))],
)
async def update_an_event(
    event_uid: str,
    book_update_data: EventUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access_token_bearer),
) -> dict:
    updated_book = await event_service.update_event(
        event_uid, book_update_data, session
    )
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return updated_book


@event_router.delete(
    "/{event_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RoleChecker(["admin", "organizer"]))],
)
async def delete_an_event(
    event_uid: str,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access_token_bearer),
):
    book_to_delete = await event_service.delete_event(event_uid, session)
    if not book_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return None


@event_router.get(
    "/search/",
    response_model=List[Event],
    dependencies=[Depends(RoleChecker(["admin", "organizer", "user"]))],
)
async def search_events(
    query: str,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access_token_bearer),
):
    events = await event_service.search_events(query, session)
    return events


@event_router.get(
    "/filter/",
    response_model=List[Event],
    dependencies=[Depends(RoleChecker(["admin", "organizer", "user"]))],
)
async def event_filter(
    date_start: str = None,
    date_end: str = None,
    location: str = None,
    category: str = None,
    organizer: str = None,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access_token_bearer),
):
    # Pass the query parameters to the service method
    events = await event_service.filter_events(
        session=session,
        date_start=date_start,
        date_end=date_end,
        location=location,
        category=category,
        organizer=organizer,
    )
    return events


@event_router.get(
    "/pagination/",
    response_model=List[Event],
    dependencies=[Depends(RoleChecker(["admin", "organizer", "user"]))],
)
async def paginated_events(
    page: int = 1,
    size: int = 10,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access_token_bearer),
):
    events = await event_service.get_paginated_events(session, page, size)
    return events
