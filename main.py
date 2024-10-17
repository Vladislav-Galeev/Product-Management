from fastapi import Depends, FastAPI
from db import create_db_and_tables, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models import Product, ProductCreate, ProductUpdate, Category, CategoryCreate


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@app.get("/")
async def home():
    return {"message": "Добро пожаловать в управление продуктами!"}


@app.get("/products/")
async def get_products(session: AsyncSession = Depends(get_session)):
    products = await session.execute(select(Product))
    return products.mappings().all()


@app.get("/products/{product_id}/")
async def get_product_by_id(product_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Product).filter(Product.id == product_id))
    product = result.mappings().all()
    if not product:
        return {"message": "Такого продукта нет!"}
    return product


@app.post("/products/")
async def create_product(product_create: ProductCreate, session: AsyncSession = Depends(get_session)):
    product = Product.model_validate(product_create)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@app.put("/products/{product_id}/")
async def update_product(product_id: int, product_update: ProductUpdate, session: AsyncSession = Depends(get_session)):
    product = await session.get(Product, product_id)
    if not product:
        return {"message": "Такого продукта нет!"}
    product_data = product_update.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(product, key, value)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@app.delete("/products/{product_id}/")
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    product = await session.get(Product, product_id)
    if not product:
        return {"message": "Такого продукта нет!"}
    await session.delete(product)
    await session.commit()
    return {"message": "Удалено!"}


@app.get("/categories/")
async def get_categories(session: AsyncSession = Depends(get_session)):
    categories = await session.execute(select(Category))
    return categories.mappings().all()


@app.post("/categories/")
async def create_category(category_create: CategoryCreate, session: AsyncSession = Depends(get_session)):
    category = Category.model_validate(category_create)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


@app.get("/products/filter/price")
async def filter_product_by_price(min: float, max: float, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Product).filter(Product.price <= max, Product.price >= min))
    product = result.mappings().all()
    if not product:
        return {"message": "Не нашлось!"}
    return product


@app.get("/products/filter/category")
async def filter_product_by_category(category_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Product).filter(Product.category_id == category_id))
    product = result.mappings().all()
    if not product:
        return {"message": "Не нашлось!"}
    return product