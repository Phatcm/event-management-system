from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import EventCreateModel, EventUpdateModel
from .models import Event
from sqlmodel import select, desc


class EventService:
    async def get_all_events(self, session: AsyncSession):
        statement = select(Event).order_by(
            desc(Event.created_at)
        )  # Return all event order by created_at col

        result = await session.exec(statement)

        return result.all()

    async def get_event(self, event_uid: str, session: AsyncSession):
        statement = select(Event).where(
            Event.uid == event_uid
        )  # Return the event match input uid

        result = await session.exec(statement)

        return result.first()

    async def create_event(self, event_data: EventCreateModel, session: AsyncSession):
        event_data_dict = event_data.model_dump()  # Turn the input data into a dict

        new_event = Event(
            **event_data_dict
        )  # Create a new Event instance with the input data

        session.add(new_event)

        await session.commit()

        return new_event

    async def update_event(
        self, event_uid: str, update_data: EventUpdateModel, session: AsyncSession
    ):
        event_to_update = await self.get_event(
            event_uid, session
        )  # Get the event to update

        if event_to_update is not None:
            update_data_dict = update_data.model_dump()

            for key, value in update_data_dict.items():  # Loop to update the values
                setattr(event_to_update, key, value)

            await session.commit()

            return event_to_update
        else:
            raise ValueError(f"Event with uid {event_uid} not found")

    async def delete_event(self, event_uid: str, session: AsyncSession):
        event_to_delete = await self.get_event(
            event_uid, session
        )  # Get the event to update

        if event_to_delete is not None:
            await session.delete(event_to_delete)

            await session.commit()

            return event_to_delete
        else:
            raise ValueError(f"Event with uid {event_uid} not found")
