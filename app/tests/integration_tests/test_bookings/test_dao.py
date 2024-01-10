from datetime import datetime

from app.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime('2023-07-10', '%Y-%m-%d'),
        date_to=datetime.strptime('2023-07-15', '%Y-%m-%d'),
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None


async def test_booking_CRUD_scenario():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime('2023-07-10', '%Y-%m-%d'),
        date_to=datetime.strptime('2023-07-15', '%Y-%m-%d'),
    )
    new_booking_id = new_booking.id

    assert new_booking.id == new_booking_id

    created_booking = await BookingDAO.find_by_id(new_booking_id)

    assert new_booking.room_id == created_booking.room_id
    assert new_booking.date_from == created_booking.date_from
    assert new_booking.date_to == created_booking.date_to

    delete_response = await BookingDAO.delete(created_booking.id, created_booking.user_id)

    deleted_booking = await BookingDAO.find_by_id(delete_response.id)

    assert not deleted_booking
