from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models.review import Review as ReviewModel
from schemas.review import Review as ReviewSchema, ReviewCreate as ReviewCreateSchema

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ReviewSchema)
def create_review(review: ReviewCreateSchema, db: Session = Depends(get_db)):
    db_review = ReviewModel(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return ReviewSchema.from_orm(db_review)


@router.get("/", response_model=List[ReviewSchema])
def read_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reviews = db.query(ReviewModel).offset(skip).limit(limit).all()
    return [ReviewSchema.from_orm(review) for review in reviews]


@router.get("/{review_id}", response_model=ReviewSchema)
def read_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return ReviewSchema.from_orm(review)


@router.put("/{review_id}", response_model=ReviewSchema)
def update_review(review_id: int, review: ReviewCreateSchema, db: Session = Depends(get_db)):
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    for key, value in review.dict().items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return ReviewSchema.from_orm(db_review)


@router.delete("/{review_id}", response_model=ReviewSchema)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(db_review)
    db.commit()
    return ReviewSchema.from_orm(db_review)
