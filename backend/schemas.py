import uuid
from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str
    last_name: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]


class SEventAdd(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    location: str


class SEvent(SEventAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SRegistration(BaseModel):
    id: int
    user_id: int
    event_id: int