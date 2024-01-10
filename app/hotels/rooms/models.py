from typing import Optional

from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Rooms(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    services: Mapped[list[str]] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]

    hotel = relationship('Hotels', back_populates='rooms')    # : Mapped[Hotels]
    booking = relationship('Bookings', back_populates='room')    # : Mapped[Bookings]

    def __str__(self):
        return f'Room #{self.id}'

# Old style version fields
# class Rooms(Base):
#     __tablename__ = "rooms"

#     id = Column(Integer, primary_key=True)
#     hotel_id = Column(ForeignKey("hotels.id"), )
#     name = Column(String, )
#     description = Column(String, nullable=True)
#     price = Column(Integer, )
#     services = Column(JSON, nullable=True)
#     quantity = Column(Integer, )
    # image_id = Column(Integer)

#     hotel = relationship("Hotels", back_populates="rooms")
#     booking = relationship("Bookings", back_populates="room")

#     def __str__(self):
#         return f"Room {self.name}"
