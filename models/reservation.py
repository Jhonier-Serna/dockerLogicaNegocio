from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    event = relationship("Event", back_populates="reservations")
    user = relationship("User", back_populates="reservations")
    review = relationship("Review", back_populates="reservation", uselist=False)
