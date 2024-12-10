import asyncio
from datetime import datetime
import json
import pytest
from sqlalchemy import insert

from app.database import Base, async_session_maker, engine
from app.config import settings

from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users
from app.bookings.models import Bookings
print("!!!", settings.MODE)

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    # print("""
    #       ////////////////////////////////
    #       ////////////////////////////////
    #       ////////////////////////////////
    #       ////////////////////////////////
    #       ////////////////////////////////
    #       ////////////////////////////////
    #       ////////////////////////////////
    #       ////////////////////////////////
    #       """)
    assert settings.MODE == "TEST"
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json") as file:
            return json.load(file)
        
    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")
    
    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)
        
        for booking in bookings:
            booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
            booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")
        
        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)
        
        await session.commit()
    

# Взято из документации к pytest-asyncio
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()