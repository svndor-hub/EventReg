from datetime import datetime
from typing import List, AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_async_engine("sqlite+aiosqlite:///app.db")
session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Model):
    first_name: Mapped[str]
    last_name: Mapped[str]

    registrations: Mapped[List["RegistrationOrm"]] = relationship(back_populates="user")


class EventOrm(Model):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    location: Mapped[str]

    registrations: Mapped[List["RegistrationOrm"]] = relationship(back_populates="event")


class RegistrationOrm(Model):
    __tablename__ = "registrations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))

    user: Mapped["User"] = relationship(back_populates="registrations")
    event: Mapped["EventOrm"] = relationship(back_populates="registrations")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session() as db:
        yield db


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
