from datetime import date
from typing import List

from sqlalchemy import select

from app.dao.base import BaseDAO
from app.hotels.dependencies import check_hotel_availability
from app.hotels.models import Hotels
from app.database import async_session_maker


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_hotels(cls,
                         location: str,
                         date_from: date,
                         date_to: date) -> List[Hotels]:

        async with async_session_maker() as session:
            hotels_query = select(Hotels).filter(Hotels.location.like(f'%{location}%'))
            hotels_data = await session.execute(hotels_query)
            hotels = hotels_data.mappings().all()
            hotels_with_rooms = []

            for hotel in hotels:
                hotel_id = hotel['Hotels'].id
                rooms_left = await check_hotel_availability(hotel_id, date_from, date_to)
                hotel = dict(hotel)
                hotel['rooms_left'] = rooms_left
                if rooms_left > 0:
                    hotels_with_rooms.append(hotel)

            return hotels_with_rooms
