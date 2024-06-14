from pydantic import BaseModel
from schemas.reservation import Reservation


class ReviewBase(BaseModel):
    comentario: str
    calificacion: int


class ReviewCreate(ReviewBase):
    reservation_id: int


class Review(ReviewBase):
    id: int
    reservation: Reservation

    class Config:
        from_attributes = True
