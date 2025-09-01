from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import models, schemas, database

router = APIRouter(prefix="/progress", tags=["ScraperProgress"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.ScraperProgress)
def set_progress(progress: schemas.ScraperProgressBase, db: Session = Depends(get_db)):
    db_progress = db.query(models.ScraperProgress).filter(models.ScraperProgress.category == progress.category).first()
    if db_progress:
        db_progress.last_page = progress.last_page
    else:
        db_progress = models.ScraperProgress(**progress.dict())
        db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress


@router.get("/{category}", response_model=schemas.ScraperProgress)
def get_progress(category: str, db: Session = Depends(get_db)):
    return db.query(models.ScraperProgress).filter(models.ScraperProgress.category == category).first()
