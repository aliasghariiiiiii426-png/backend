from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    store_url = Column(String, unique=True, index=True)
    category = Column(String, index=True)
    instagram = Column(String, nullable=True)
    facebook = Column(String, nullable=True)
    telegram = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    tiktok = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    last_scraped = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    products = relationship("Product", back_populates="store", cascade="all, delete")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"))
    product_id = Column(String, unique=True, index=True)
    title = Column(String)
    handle = Column(String)
    body_html = Column(Text)
    vendor = Column(String)
    product_type = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    published_at = Column(DateTime)
    tags = Column(Text)

    store = relationship("Store", back_populates="products")
    variants = relationship("Variant", back_populates="product", cascade="all, delete")
    images = relationship("Image", back_populates="product", cascade="all, delete")


class Variant(Base):
    __tablename__ = "variants"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    variant_id = Column(String, unique=True, index=True)
    title = Column(String)
    sku = Column(String)
    price = Column(String)
    available = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    position = Column(Integer)

    product = relationship("Product", back_populates="variants")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    image_id = Column(String, unique=True, index=True)
    src = Column(Text)
    position = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    product = relationship("Product", back_populates="images")


class ScraperProgress(Base):
    __tablename__ = "scraper_progress"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, unique=True, index=True)
    last_page = Column(Integer, default=1)