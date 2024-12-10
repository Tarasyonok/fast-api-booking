from datetime import date
from sqlalchemy import insert, select, func, and_, or_
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.database import engine, async_session_maker


class RoomDAO(BaseDAO):
    model = Rooms
    
    @classmethod
    async def find_all(
        cls,
        hotel_id: int,
        # date_from: date,
        # date_to: date,
    ):
        async with async_session_maker() as session:
            query = select(Rooms).filter(Rooms.hotel_id == hotel_id)
            result = await session.execute(query)
            return result.mappings().all()
        
     