from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.db import models, schemas, database
from typing import List, Dict, Any

router = APIRouter(prefix="/stores", tags=["Stores"])


@router.post("/", response_model=schemas.Store)
async def create_or_update_store(
    store: schemas.StoreCreate,
    db: AsyncSession = Depends(database.get_db)
):
    result = await db.execute(
        select(models.Store).where(models.Store.store_url == store.store_url)
    )
    db_store = result.scalar_one_or_none()

    if db_store:
        for key, value in store.dict().items():
            setattr(db_store, key, value)
    else:
        db_store = models.Store(**store.dict())
        db.add(db_store)

    await db.commit()
    await db.refresh(db_store)
    return db_store


@router.get("/", response_model=Dict[str, Any])
async def list_stores(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return"),
    db: AsyncSession = Depends(database.get_db)
):
    # Total count
    result = await db.execute(select(func.count(models.Store.id)))
    total = result.scalar_one()

    # Paginated stores
    result = await db.execute(
        select(models.Store).offset(skip).limit(limit)
    )
    stores = result.scalars().all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "stores": stores
    }


@router.get("/{store_id}", response_model=schemas.Store)
async def get_store(store_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(
        select(models.Store).where(models.Store.id == store_id)
    )
    db_store = result.scalar_one_or_none()

    if not db_store:
        raise HTTPException(status_code=404, detail=f"Store {store_id} not found")

    return db_store


@router.put("/{store_id}", response_model=schemas.Store)
async def update_store(
    store_id: int,
    store: schemas.StoreCreate,
    db: AsyncSession = Depends(database.get_db)
):
    result = await db.execute(
        select(models.Store).where(models.Store.id == store_id)
    )
    db_store = result.scalar_one_or_none()

    if not db_store:
        raise HTTPException(status_code=404, detail=f"Store {store_id} not found")

    for key, value in store.dict().items():
        setattr(db_store, key, value)

    await db.commit()
    await db.refresh(db_store)
    return db_store


@router.delete("/{store_id}", response_model=dict)
async def delete_store(store_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(
        select(models.Store).where(models.Store.id == store_id)
    )
    db_store = result.scalar_one_or_none()

    if not db_store:
        raise HTTPException(status_code=404, detail=f"Store {store_id} not found")

    await db.delete(db_store)
    await db.commit()

    return {"status": "ok", "message": f"Store {store_id} deleted"}
