import json
import uuid
from pathlib import Path
from typing import AsyncGenerator, List
import pytest_asyncio
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from webapp.db.postgres import engine, get_session
from webapp.models.meta import metadata


@pytest_asyncio.fixture()
async def client(app: FastAPI):
    async with AsyncClient(app=app, base_url='http://test.com') as client:
        yield client


@pytest_asyncio.fixture()
async def db_session(app: FastAPI) -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as connection:
        session_maker = async_sessionmaker(bind=connection)
        session = session_maker()

        yield session

        await connection.rollback()


@pytest_asyncio.fixture()
async def _load_fixtures(db_session: AsyncSession, fixtures: List[Path]):
    for fixture in fixtures:
        model = metadata.tables[fixture.stem]

        with open(fixture, 'r') as file:
            values = json.load(file)
        await db_session.execute(insert(model).values(values))
        await db_session.commit()
        print((await db_session.execute(select(model))).all())

    return


@pytest_asyncio.fixture()
async def _common_api_fixture(
    _load_fixtures,
) -> None:
    return
