from fastapi import FastAPI
from app.db import models, database
from app.routers import stores, products, scraper_progress

# create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Shopify Scraper Backend")

@app.get("/health")
def health():
    return {"status": "ok"}

# include routers
app.include_router(stores.router)
app.include_router(products.router)
app.include_router(scraper_progress.router)
