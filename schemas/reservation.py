from pydantic import BaseModel
from schemas.event import Event
from schemas.user import User


class ReservationBase(BaseModel):
    event_id: int
    user_id: int


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int
    event: Event
    user: User

    class Config:
        from_attributes = True
