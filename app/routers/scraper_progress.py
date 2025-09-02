from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import models, schemas, database

router = APIRouter(prefix="/progress", tags=["ScraperProgress"])


@router.post("/", response_model=schemas.ScraperProgress)
async def set_progress(
    progress: schemas.ScraperProgressBase,
    db: AsyncSession = Depends(database.get_db)
):
    # Check if progress exists for this category
    result = await db.execute(
        select(models.ScraperProgress).where(models.ScraperProgress.category == progress.category)
    )
    db_progress = result.scalar_one_or_none()

    if db_progress:
        db_progress.last_page = progress.last_page
    else:
        db_progress = models.ScraperProgress(**progress.dict())
        db.add(db_progress)

    await db.commit()
    await db.refresh(db_progress)
    return db_progress


@router.get("/{category}", response_model=schemas.ScraperProgress)
async def get_progress(category: str, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(
        select(models.ScraperProgress).where(models.ScraperProgress.category == category)
    )
    db_progress = result.scalar_one_or_none()

    if not db_progress:
        raise HTTPException(status_code=404, detail=f"Progress for category '{category}' not found")

    return db_progress