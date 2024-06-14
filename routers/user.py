from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models.user import User as UserModel
from schemas.user import User as UserSchema, UserCreate as UserCreateSchema

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserSchema.from_orm(db_user)


@router.get("/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return [UserSchema.from_orm(user) for user in users]


@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserSchema.from_orm(user)

@router.get("/search/{user_email}", response_model=UserSchema)
def read_userEmail(user_email, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserSchema.from_orm(user)


@router.put("/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return UserSchema.from_orm(db_user)


@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return UserSchema.from_orm(db_user)


