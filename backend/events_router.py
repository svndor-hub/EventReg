from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from database import User
from repository import EventRepository, RegistrationRepository
from schemas import SEventAdd, SRegistration
from users import fastapi_users

events_router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

current_user = fastapi_users.current_user()

@events_router.post("")
async def create_event(event_data: SEventAdd) -> int:
    event_id = await EventRepository.add_event(event_data)
    return event_id


@events_router.get("")
async def get_events() -> list[SEventAdd]:
    events = await EventRepository.find_all()
    return events


@events_router.get("/{event_id}")
async def get_event(event_id: int) -> SEventAdd:
    event = await EventRepository.find_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@events_router.post("/{event_id}/register")
async def register_event(event_id: int, user: User = Depends(current_user)) -> int:
    registration_id = await RegistrationRepository.register(event_id, user.id)
    return registration_id


@events_router.get("/{event_id}/registrations")
async def get_registrations(event_id: int, user: User = Depends(current_user)) -> list[SRegistration]:
    event = await EventRepository.find_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if user.is_superuser:
        return event.registrations
    else:
        raise HTTPException(status_code=403)


@events_router.delete("/{event_id}/unregister", status_code=201)
async def unregister_event(event_id: int, user: User = Depends(current_user)):
    await RegistrationRepository.unregister(event_id, user.id)
    return {'message': 'Unregistered successfully'}