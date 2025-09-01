from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import models, schemas, database
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{store_id}", response_model=dict)
def add_products(store_id: int, products: List[schemas.ProductCreate], db: Session = Depends(get_db)):
    for p in products:
        db_product = models.Product(**p.dict(), store_id=store_id)
        db.merge(db_product)  # insert or update
    db.commit()
    return {"status": "ok", "count": len(products)}
