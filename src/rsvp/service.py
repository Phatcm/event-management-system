from sqlmodel.ext.asyncio.session import AsyncSession

# from .schemas import EventCreateModel, EventUpdateModel
from src.db.models import RSVP
from src.db.models import Event
from sqlmodel import select, desc
from typing import List, Optional


class RSVPService:
    async def get_rsvps_of_user(
        self, user_uid: str, session: AsyncSession
    ) -> List[RSVP]:
        # Fetch all RSVPs for a specific user
        statement = select(RSVP).where(RSVP.user_uid == user_uid)
        result = await session.exec(statement)
        return result.all()  # Return all the results as a list

    async def get_rsvp(self, rsvp_uid: str, session: AsyncSession) -> Optional[RSVP]:
        # Fetch a specific RSVP by its UID
        statement = select(RSVP).where(RSVP.uid == rsvp_uid)
        result = await session.exec(statement)
        rsvp = result.first()  # Use first() to get the first result or None
        return rsvp  # Return the result, which can be None or the found RSVP

    async def get_event(self, event_uid: str, session: AsyncSession) -> Optional[Event]:
        # Fetch a specific event by its UID
        statement = select(Event).where(Event.uid == event_uid)
        result = await session.exec(statement)
        event = result.first()  # Use first() to get the first result or None
        return event  # Return the result, which can be None or the found event

    async def rsvp_event(self, event_uid: str, user_uid: str, session: AsyncSession):
        # check for duplicate rsvp using is_user_rsvp()
        if await self.is_user_rsvp(event_uid, user_uid, session):
            raise ValueError(
                f"User {user_uid} has already RSVPed for event {event_uid}."
            )  # Raise error

        # check if event exist
        event = await self.get_event(event_uid, session)
        if not event:
            raise ValueError(f"Event with UID {event_uid} does not exist.")

        rsvp_count = await self.get_event_rsvp_count(event_uid, session)
        if rsvp_count >= event.capacity:
            raise ValueError(f"Event with UID {event_uid} is already full.")

        rsvp = RSVP(event_uid=event_uid, user_uid=user_uid)
        session.add(rsvp)
        await session.commit()
        return rsvp

    async def is_user_rsvp(
        self, event_uid: str, user_uid: str, session: AsyncSession
    ) -> bool:
        result = await session.exec(
            select(RSVP).where(RSVP.event_uid == event_uid, RSVP.user_uid == user_uid)
        )
        return result.first() is not None

    async def cancel_rsvp(self, rsvp_uid: str, session: AsyncSession):
        rsvp_to_cancel = await self.get_rsvp(rsvp_uid, session)
        if rsvp_to_cancel:
            await session.delete(rsvp_to_cancel)
            await session.commit()
            return rsvp_to_cancel
        else:
            raise ValueError(f"RSVP with uid {rsvp_uid} not found")

    async def get_event_rsvp_count(self, event_uid: str, session: AsyncSession) -> int:
        result = await session.exec(select(RSVP).where(RSVP.event_uid == event_uid))
        return len(result.all())  # Use count() to get the number of rows
