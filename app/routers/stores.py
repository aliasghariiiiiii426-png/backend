from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import models, schemas, database

router = APIRouter(prefix="/stores", tags=["Stores"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Store)
def create_or_update_store(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    db_store = db.query(models.Store).filter(models.Store.store_url == store.store_url).first()
    if db_store:
        for key, value in store.dict().items():
            setattr(db_store, key, value)
    else:
        db_store = models.Store(**store.dict())
        db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


@router.get("/{store_id}", response_model=schemas.Store)
def get_store(store_id: int, db: Session = Depends(get_db)):
    return db.query(models.Store).filter(models.Store.id == store_id).first()
