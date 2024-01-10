import asyncio
import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert

from app.bookings.models import Bookings
from app.config import settings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users
from app.database import Base, async_session_maker, engine
from main import app as fastapi_app


@pytest.fixture(scope='function', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def _open_mock_json(model: str):
        with open(f'app/tests/mock_{model}.json', 'r') as file:
            return json.load(file)

    hotels = _open_mock_json('hotels')
    rooms = _open_mock_json('rooms')
    users = _open_mock_json('users')
    bookings = _open_mock_json('bookings')

    for item in bookings:
        item['date_from'] = datetime.strptime(item['date_from'], '%Y-%m-%d').date()
        item['date_to'] = datetime.strptime(item['date_to'], '%Y-%m-%d').date()

    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def async_client():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
async def authenticated_async_client():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        await ac.post('/auth/login', json={
            'email': 'test@test.com',
            'password': 'test'
        })
        assert ac.cookies['booking_access_token']
        yield ac


@pytest.fixture(scope='function')
async def session():
    async with async_session_maker() as session:
        yield session

