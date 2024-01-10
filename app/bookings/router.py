from datetime import date

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import join, select

from app.bookings.dao import BookingDAO
from app.bookings.models import Bookings
from app.bookings.schemas import SBooking
from app.exceptions import BookingNotFound, RoomCannotBeBooked
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.database import async_session_maker

router = APIRouter(
    prefix='/bookings',
    tags=['Bookings']
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingDAO.get_bookings(user_id=user.id)


@router.post('')
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    booking_dict = SBooking.model_validate(booking).model_dump()
    if not booking:
        raise RoomCannotBeBooked
    # send_booking_confirmation_email.delay(booking_dict, user.email)

    return booking_dict


@router.delete('/{booking_id}')
async def delete_bookings(booking_id: int, user: Users = Depends(get_current_user)):
    existing_booking = await BookingDAO.delete(booking_id, user.id)
    if not existing_booking:
        raise BookingNotFound
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/example/no_orm')
async def get_noorm():
    async with async_session_maker() as session:
        query = select(Rooms.__table__.columns, Hotels.__table__.columns, Bookings.__table__.columns
                       ).join(Hotels, Rooms.hotel_id == Hotels.id
                              ).join(Bookings, Bookings.room_id == Rooms.id)

        res = await session.execute(query)
        return res.mappings().all()
