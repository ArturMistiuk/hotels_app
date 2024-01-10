from fastapi import APIRouter, Response, status

from app.exceptions import (IncorrectEmailOrPasswordError,
                            UserAlreadyExistsError)
from app.users.auth import (authenticate_user, create_access_token,
                            get_password_hash)
from app.users.dao import UsersDAO
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register')
async def register_user(user_data: SUserAuth) -> Response:
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsError
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)

    return Response(status_code=status.HTTP_201_CREATED)


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordError
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return {'access_token': access_token}
