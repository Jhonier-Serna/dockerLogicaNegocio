from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import event, user, reservation, review

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event.router, prefix="/events", tags=["events"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(reservation.router, prefix="/reservations", tags=["reservations"])
app.include_router(review.router, prefix="/reviews", tags=["reviews"])
#docker-compose up --build