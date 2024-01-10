import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('email, password, status_code', [
    ('kotpes@gmail.com', 'kotopes', 201),
    ('abcde', 'pesokot', 422),
])
async def test_register_user(email, password, status_code, async_client: AsyncClient):
    response = await async_client.post('/auth/register', json={
        'email': email,
        'password': password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize('email, password, status_code', [
    ("test@test.com", 'test', 200),
    ('nouser@gmail.com', 'test', 401),
    ('abcd', 'test', 422),
])
async def test_login_user(email, password, status_code, async_client: AsyncClient):
    response = await async_client.post('/auth/login', json={
        'email': email,
        'password': password,
    })

    assert response.status_code == status_code
