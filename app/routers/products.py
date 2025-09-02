from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import models, schemas, database

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/{store_id}", response_model=dict)
async def add_product(
    store_id: int,
    product: schemas.ProductCreate,
    db: AsyncSession = Depends(database.get_db)
):
    # Validate store exists
    result = await db.execute(select(models.Store).where(models.Store.id == store_id))
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail=f"Store {store_id} not found")

    db_product = models.Product(**product.dict(), store_id=store_id)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)

    return {"status": "ok", "product_id": db_product.id}


@router.put("/{store_id}/{product_id}", response_model=dict)
async def update_product(
    store_id: int,
    product_id: int,
    product: schemas.ProductCreate,
    db: AsyncSession = Depends(database.get_db)
):
    # Validate store exists
    result = await db.execute(select(models.Store).where(models.Store.id == store_id))
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail=f"Store {store_id} not found")

    result = await db.execute(
        select(models.Product).where(
            models.Product.id == product_id,
            models.Product.store_id == store_id
        )
    )
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found in store {store_id}")

    for key, value in product.dict().items():
        setattr(db_product, key, value)

    await db.commit()
    await db.refresh(db_product)

    return {"status": "ok", "product_id": db_product.id}