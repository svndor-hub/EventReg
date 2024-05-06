from uuid import UUID

from fastapi import HTTPException

from database import session, EventOrm, RegistrationOrm
from schemas import SEventAdd, SEvent

from sqlalchemy import select


class EventRepository:
    @classmethod
    async def add_event(cls, data: SEventAdd) -> int:
        async with session() as db:
            event_dict = data.model_dump()

            event = EventOrm(**event_dict)
            db.add(event)
            await db.flush()
            await db.commit()

            return event.id

    @classmethod
    async def find_all(cls) -> list[SEvent]:
        async with session() as db:
            query = select(EventOrm)
            result = await db.execute(query)
            event_models = result.scalars().all()
            event_schemas = [SEvent.model_validate(event_model) for event_model in event_models]
            return event_schemas

    @classmethod
    async def find_by_id(cls, event_id) -> SEvent:
        async with session() as db:
            query = select(EventOrm).filter_by(id=event_id)
            result = await db.execute(query)
            event_model = result.scalars().first()
            event_schema = SEvent.model_validate(event_model)
            return event_schema


class RegistrationRepository:
    @classmethod
    async def register(cls, event_id: int, user_id: UUID) -> int:
        async with session() as db:
            registration = RegistrationOrm(event_id=event_id, user_id=user_id)
            db.add(registration)
            await db.flush()
            await db.commit()
            return registration.id

    @classmethod
    async def unregister(cls, event_id: int, user_id: UUID):
        async with session() as db:
            query = select(RegistrationOrm).filter_by(user_id=user_id, event_id=event_id)
            result = await db.execute(query)
            registration = result.scalars().first()
            if not registration:
                raise HTTPException(status_code=404, detail="Registration not found")

            await db.delete(registration)
            await db.commit()
