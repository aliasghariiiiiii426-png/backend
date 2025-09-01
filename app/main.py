from fastapi import FastAPI
from db import models, database
from routers import stores, products, scraper_progress

# create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Shopify Scraper Backend")

# include routers
app.include_router(stores.router)
app.include_router(products.router)
app.include_router(scraper_progress.router)
