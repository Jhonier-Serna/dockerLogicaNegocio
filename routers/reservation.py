from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models.reservation import Reservation as ReservationModel
from schemas.reservation import Reservation as ReservationSchema, ReservationCreate as ReservationCreateSchema

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ReservationSchema)
def create_reservation(reservation: ReservationCreateSchema, db: Session = Depends(get_db)):
    db_reservation = ReservationModel(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return ReservationSchema.from_orm(db_reservation)


@router.get("/", response_model=List[ReservationSchema])
def read_reservations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reservations = db.query(ReservationModel).offset(skip).limit(limit).all()
    return [ReservationSchema.from_orm(reservation) for reservation in reservations]


@router.get("/{reservation_id}", response_model=ReservationSchema)
def read_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return ReservationSchema.from_orm(reservation)


@router.put("/{reservation_id}", response_model=ReservationSchema)
def update_reservation(reservation_id: int, reservation: ReservationCreateSchema, db: Session = Depends(get_db)):
    db_reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    for key, value in reservation.dict().items():
        setattr(db_reservation, key, value)
    db.commit()
    db.refresh(db_reservation)
    return ReservationSchema.from_orm(db_reservation)


@router.delete("/{reservation_id}", response_model=ReservationSchema)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(db_reservation)
    db.commit()
    return ReservationSchema.from_orm(db_reservation)
