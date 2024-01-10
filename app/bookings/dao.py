from datetime import date

from sqlalchemy import and_, delete, insert, select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.dependencies import check_room_availability
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.models import Rooms
from app.loggger import logger
from app.database import async_session_maker


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def get_bookings(cls, user_id: int):
        bookings = await BookingDAO.find_all(user_id=user_id)

        bookings = [
            {
                **booking,
                'image_id': room.image_id,
                'name': room.name,
                'description': room.description,
                'services': room.services,
            }
            for booking in bookings
            for room in [await RoomsDAO.find_by_id(model_id=booking['room_id'])]]

        return bookings

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        """
        WITH booked_rooms AS (
            SELECT id, room_id, user_id, date_from, date_to, price, total_cost, total_days
            FROM bookings
            WHERE room_id = 1 AND
            date_from <= '2023-06-25' AND date_to >= '2023-07-10'
        )

        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id;
        """
        try:
            async with async_session_maker() as session:
                rooms_left = await check_room_availability(room_id, date_from, date_to)

                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price = price.scalar()
                    add_booking = insert(Bookings).values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    ).returning(Bookings)

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()
                else:
                    return None
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = 'Database Exception'
            elif isinstance(e, Exception):
                msg = 'Unknown Exception'
            msg += ': Cannot add booking'
            extra = {
                'room_id': room_id,
                'user_id': user_id,
                'date_from': date_from,
                'date_to': date_to,
            }
            logger.error(msg, extra=extra, exc_info=True)

    @classmethod
    async def delete(cls, booking_id: int, user_id: int):
        """
        DELETE FROM bookings
            WHERE id = 1 AND user_id = 1
        """

        async with async_session_maker() as session:
            existing_booking = await session.execute(
                select(Bookings).where(and_(Bookings.id == booking_id, Bookings.user_id == user_id))
            )
            try:
                existing_booking = existing_booking.scalar_one()
            except NoResultFound:
                return None
            delete_query_for_booking = delete(Bookings).where(Bookings.id == booking_id, Bookings.user_id == user_id)
            await session.execute(delete_query_for_booking)
            await session.commit()
            return existing_booking
