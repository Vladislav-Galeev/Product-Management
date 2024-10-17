from fastapi import Depends
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session


class CategoryBase(SQLModel):
    name: str


class Category(CategoryBase, table=True):
    id: int = Field(default=None, primary_key=True)

    products: list["Product"] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class ProductBase(SQLModel):
    name: str
    description: str
    price: float = Field(ge=0)
    count: int = Field(ge=0)
    
    category_id: int | None = Field(default=None, foreign_key="category.id")


class Product(ProductBase, table=True):
    id: int = Field(default=None, primary_key=True)

    category: Category | None = Relationship(back_populates="products")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, ge=0)
    count: int = Field(default=None, ge=0)
    category_id: int | None = None