import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('location, date_from, date_to, status_code', [
    ('Komi', '2023-01-01', '2023-01-02', 200),
    ('Zapor', '2023-01-01', '2023-01-02', 409),
    ('Komi', '2023-01-02', '2023-01-01', 400),
    ('Komi', '2023-01-01', '2023-02-03', 400),
])
async def test_get_hotels(location: str, date_from: str, date_to: str, status_code, async_client: AsyncClient):
    response = await async_client.get(f'/hotels/{location}', params={
        'location': location,
        'date_from': date_from,
        'date_to': date_to,
    })

    assert response.status_code == status_code
