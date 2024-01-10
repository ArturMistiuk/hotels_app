from app.bookings.dao import BaseDAO
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users
