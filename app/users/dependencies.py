from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (IncorrectTokenFormatError, TokenAbsentError,
                            TokenExpiredError, UserIsNotPresentError)
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokenAbsentError
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatError
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredError
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIsNotPresentError
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentError

    return user
