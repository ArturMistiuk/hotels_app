import asyncio
from datetime import date, timedelta

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions import IncorrectBookingDate, RoomCannotBeBooked
from app.hotels.dao import HotelsDAO

router = APIRouter(
    prefix='/hotels',
    tags=['hotels']
)


@router.get('/{location}')
@cache(expire=30)
async def get_hotels(location: str, date_from: date, date_to: date):
    if date_from >= date_to or date_to - date_from > timedelta(days=30):
        raise IncorrectBookingDate
    hotels = await HotelsDAO.get_hotels(location, date_from, date_to)
    if not hotels:
        raise RoomCannotBeBooked
    return hotels


@router.get('/id/{hotel_id}')
async def get_hotel(hotel_id: int):
    hotel = await HotelsDAO.find_by_id(model_id=hotel_id)

    return hotel
