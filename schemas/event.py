from pydantic import BaseModel
from typing import List
from datetime import date, time


class EventBase(BaseModel):
    eventName: str
    category: str
    date: date
    places: int
    startTime: time
    endTime: time
    place: str
    entityInCharge: str
    description: str
    fileLinks: List[str]


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int

    class Config:
        from_attributes = True
