from fastapi import HTTPException, status


class BookingError(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsError(BookingError):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User with this email already exists'


class IncorrectEmailOrPasswordError(BookingError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Incorrect email or password'


class TokenExpiredError(BookingError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token expired'


class TokenAbsentError(BookingError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token absent'


class IncorrectTokenFormatError(BookingError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Incorrect token format'


class UserIsNotPresentError(BookingError):
        status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingError):
    status_code = status.HTTP_409_CONFLICT
    detail = 'No available rooms'


class BookingNotFound(BookingError):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Booking not found'


class IncorrectBookingDate(BookingError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Incorrect date for booking'

