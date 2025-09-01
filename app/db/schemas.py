from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class StoreBase(BaseModel):
    store_url: str
    category: str
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    telegram: Optional[str] = None
    linkedin: Optional[str] = None
    tiktok: Optional[str] = None
    twitter: Optional[str] = None


class StoreCreate(StoreBase):
    pass


class Store(StoreBase):
    id: int
    last_scraped: Optional[datetime]

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    product_id: str
    title: str
    handle: str
    body_html: Optional[str] = None
    vendor: Optional[str] = None
    product_type: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    tags: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    store_id: int

    class Config:
        orm_mode = True


class ScraperProgressBase(BaseModel):
    category: str
    last_page: int


class ScraperProgress(ScraperProgressBase):
    id: int

    class Config:
        orm_mode = True
