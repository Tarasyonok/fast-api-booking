from datetime import date
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.bookings.models import Bookings

from sqlalchemy import select
from sqlalchemy import insert, select, func, and_, or_


class HotelDAO(BaseDAO):
    model = Hotels
    @classmethod
    async def find_by_location(cls, location: str, date_from: date, date_to: date):
        """
        -- 2023-05-15
        -- 2023-06-10
        -- SELECT Hotels.location FROM Hotels
        -- WHERE Hotels.id = 1
        WITH bookings_count AS (
            SELECT * FROM Bookings
            LEFT JOIN Rooms ON Bookings.room_id = Rooms.id
            WHERE ((date_from >= '2023-05-15' AND date_from <= '2023-06-10')
            OR (date_from <= '2023-05-15' AND date_to > '2023-05-15'))
        )
            
        WITH bookings_count AS (
            SELECT Hotels.id, Hotels.rooms_quantity - COUNT(bookings_count.hotel_id) FROM Hotels
            LEFT JOIN bookings_count ON Hotels.id = bookings_count.hotel_id
            WHERE Hotels.location LIKE '%Алтай%'
            GROUP BY Hotels.id, Hotels.rooms_quantity, bookings_count.hotel_id
        )
	"""
        async with async_session_maker() as session:
            print(Hotels.location.like(f"%{location}%"))
            get_location_hotels = select(Hotels.__table__.columns).where(Hotels.location.like(f"%{location}%"))
            location_hotels = await session.execute(get_location_hotels)
            
            # booked_rooms = select(Bookings).where(
            #     and_(
            #         Bookings.room == location_hotels.id,
            #         or_(
            #             and_(
            #                 Bookings.date_from >= date_from,
            #                 Bookings.date_from <= date_to
            #             ),
            #             and_(
            #                 Bookings.date_from <= date_from,
            #                 Bookings.date_to > date_from
            #             )
            #         )
            #     )
            # ).cte("booked_rooms")
            
            return location_hotels.mappings().all()

        
class RoomDAO(BaseDAO):
    model = Hotels
