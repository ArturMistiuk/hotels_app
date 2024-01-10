import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('room_id, date_from, date_to, status_code', [
    *[(4, '2030-01-01', '2030-01-15', 200)]*8,
])
async def test_add_and_get_booking(room_id, date_from, date_to, status_code, authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.post('/bookings', params={
        'room_id': room_id,
        'date_from': date_from,
        'date_to': date_to,
    })

    assert response.status_code == status_code


async def test_get_and_delete_bookings(authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.get('/bookings')

    assert response.status_code == 200
    assert len(response.json()) == 2

    bookings = response.json()
    for booking in bookings:
        response = await authenticated_async_client.delete(f'/bookings/{booking["id"]}')
        assert response.status_code == 204

    response = await authenticated_async_client.get('/bookings')

    assert response.status_code == 200
    assert len(response.json()) == 0
