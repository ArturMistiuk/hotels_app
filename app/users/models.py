from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]

    booking = relationship('Bookings', back_populates='user')    # : Mapped[Bookings]

    def __str__(self):
        return f'User {self.email}'

#    Old style version fields
# class Users(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, nullable=False)
#     email = Column(String, nullable=False)
#     hashed_password = Column(String, nullable=False)

#     booking = relationship("Bookings", back_populates="user")

#     def __str__(self):
#         return f"User {self.email}"
