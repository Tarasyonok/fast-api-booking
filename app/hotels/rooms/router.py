from fastapi import APIRouter
from app.hotels.router import router
from app.hotels.rooms.dao import RoomDAO

@router.get("/{hotel_id}/rooms")
async def get_hotels(hotel_id: int):
    return await RoomDAO.find_all(hotel_id)

