from datetime import date

from sqlalchemy import and_, func, select

from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker


async def check_hotel_availability(hotel_id: int, date_from: date, date_to: date):
    async with async_session_maker() as session:
        hotel_rooms_id_query = select(Rooms.id).filter(Rooms.hotel_id == hotel_id)
        hotel_rooms_id = await session.execute(hotel_rooms_id_query)
        hotel_rooms_id_tuple = hotel_rooms_id.all()
        hotel_rooms_id = {room_id[0] for room_id in hotel_rooms_id_tuple}

        available_rooms_left = 0
        for room_id in hotel_rooms_id:
            available_rooms_left += await check_room_availability(room_id, date_from, date_to)

        return available_rooms_left


async def check_room_availability(room_id: int, date_from: date, date_to: date):
    async with async_session_maker() as session:
        booked_rooms = select(Bookings).where(
            and_(
                Bookings.room_id == room_id,
                and_(
                    Bookings.date_from <= date_to,
                    Bookings.date_to >= date_from
                ),
            )
        ).cte('booked_rooms')

        get_rooms_left = select(
            (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
        ).select_from(Rooms).join(
            booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
        ).where(Rooms.id == room_id).group_by(
            Rooms.quantity, booked_rooms.c.room_id
        )

        rooms_left = await session.execute(get_rooms_left)
        rooms_left = rooms_left.scalar()

        return rooms_left
