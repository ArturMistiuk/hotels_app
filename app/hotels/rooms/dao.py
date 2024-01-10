import asyncio
from datetime import date

from app.dao.base import BaseDAO
from app.hotels.dao import HotelsDAO
from app.hotels.dependencies import check_room_availability
from app.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms(cls,
                        hotel_id: int,
                        date_from: date,
                        date_to: date):
        hotel = await HotelsDAO.find_by_id(model_id=hotel_id)

        hotel_rooms = await RoomsDAO.find_all(hotel_id=hotel.id)

        tasks = [check_room_availability(room['id'], date_from, date_to) for room in hotel_rooms]
        hotel_rooms_left = await asyncio.gather(*tasks)

        total_days = (date_to - date_from).days
        available_rooms = [
            {
                **room,
                'total_cost': room['price'] * total_days,    # add total_cost column
                'rooms_left': left    # add rooms_left column
            }
            for room, left in zip(hotel_rooms, hotel_rooms_left)
            if left > 0
        ]

        return available_rooms
