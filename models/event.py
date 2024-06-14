from sqlalchemy import Column, Integer, String, Date, Time, JSON
from sqlalchemy.orm import relationship, Session
from database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    eventName = Column(String, index=True)
    category = Column(String, index=True)
    date = Column(Date)
    places = Column(Integer)
    startTime = Column(Time)
    endTime = Column(Time)
    place = Column(String)
    entityInCharge = Column(String)
    description = Column(String)
    fileLinks = Column(JSON)

    reservations = relationship("Reservation", back_populates="event")

    def to_dict(self):
        return {
            'id': self.id,
            'eventName': self.eventName,
            'category': self.category,
            'date': self.date,
            'places': self.places,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'place': self.place,
            'entityInCharge': self.entityInCharge,
            'description': self.description,
            'fileLinks': self.fileLinks
        }

    def get_users(self, db: Session):
        return [reservation.user for reservation in self.reservations]
