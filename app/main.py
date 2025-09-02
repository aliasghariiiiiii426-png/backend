from fastapi import FastAPI
import asyncio
from app.db import models, database
from app.routers import stores, products, scraper_progress

app = FastAPI(title="Shopify Scraper Backend")


@app.get("/health")
def health():
    return {"status": "ok"}


# include routers
app.include_router(stores.router)
app.include_router(products.router)
app.include_router(scraper_progress.router)


# create tables asynchronously
async def init_models():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# run table creation at startup
@app.on_event("startup")
async def on_startup():
    await init_models()
