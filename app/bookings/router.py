from datetime import date
from fastapi import APIRouter, Depends, Request, BackgroundTasks
from pydantic import parse_obj_as
from sqlalchemy import select
from dataclasses import dataclass, asdict
from fastapi_versioning import version

from app.exceptions import RoomCannotBeBooked
from app.bookings.dao import BookingDAO
from app.bookings.models import Bookings
from app.database import async_session_maker
from app.bookings.schemas import SBooking
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)

@version(1)
@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)): # -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@version(1)
@router.post("")
async def add_booking(
    # background_tasks: BackgroundTasks,
    room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    # booking_dict = asdict(booking)
    booking_dict = {column.name: getattr(booking, column.name) for column in Bookings.__table__.columns}
    print(booking_dict)
    
    # celery
    # send_booking_confirmation_email.delay(booking_dict, user.email)
    # background_tasks
    # background_tasks.add_task(send_booking_confirmation_email(booking_dict, user.email))
    
    return booking
    
    
@version(1)
@router.delete("/{booking_id}")
async def add_booking(
    booking_id: int, user: Users = Depends(get_current_user)
):
    await BookingDAO.delete_by_id(booking_id)
    

