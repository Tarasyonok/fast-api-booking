from datetime import date
from fastapi import APIRouter
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel

from fastapi_cache.decorator import cache
import asyncio
# from app.hotels.rooms.dao import RoomDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Отели & Комнаты"],
)

@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location_and_time(location: str, date_from: date, date_to: date):# -> list[SHotel]:
    await asyncio.sleep(3)
    return await HotelDAO.find_by_location(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int):
    return await HotelDAO.find_by_id(hotel_id)


