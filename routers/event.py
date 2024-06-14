from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.event import Event as EventModel
from schemas.event import Event as EventSchema, EventCreate as EventCreateSchema

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=EventSchema)
def create_event(event: EventCreateSchema, db: Session = Depends(get_db)):
    db_event = EventModel(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return EventSchema.from_orm(db_event)


@router.get("/", response_model=List[EventSchema])
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = db.query(EventModel).offset(skip).limit(limit).all()
    return [EventSchema.from_orm(event) for event in events]


@router.get("/{event_id}", response_model=EventSchema)
def read_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventSchema.from_orm(event)


@router.put("/{event_id}", response_model=EventSchema)
def update_event(event_id: int, event: EventCreateSchema, db: Session = Depends(get_db)):
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in event.dict().items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    users = db_event.get_users(db)
    for u in users:
        payload = {
            "DestinationEmail": u.email,
            "DestinationName": u.name,
            "EmailSubject": "Cambio en fecha/horario de evento",
            "NewEventDate": f"{db_event.date} - {db_event.startTime} - {db_event.endTime}",
            "EventImageUrl": db_event.fileLinks[0],
            "EventUrl": ""
        }
        response = requests.post("https://dockernotificaciones.onrender.com/notification/ModificacionEmail", json=payload, verify=False)

        if response.status_code != 200:
            print(f"Failed to send notification to {u.email}. Status code: {response.status_code}")
        else:
            print(f"Notification sent to {u.email}")
    return EventSchema.from_orm(db_event)


@router.delete("/{event_id}", response_model=EventSchema)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return EventSchema.from_orm(db_event)
