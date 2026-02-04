from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .security import hash_password
from src.models import (
    User,
    Product,
)
from .schemas import UserSchema, CreateUser


async def create_user(session: AsyncSession, user_info: CreateUser) -> User:
    user_info.hashed_password = hash_password(user_info.hashed_password)
    user = User(**user_info.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, username: str) -> UserSchema | None:
    stmt = select(User).where(User.username == username)
    user = await session.scalar(stmt)
    return user


async def get_user_with_products(session: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    if user:
        ret = f"username: {user.username}"
        stmt = select(Product).where(Product.username == user.username)
        products: list[Product] | None = await session.scalar(stmt)
        if products:
            ret += "*" * 10
            ret += "Items for sale:"
            for product in products:
                ret += f"name: {product.name} price: {product.price}"
        return ret
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
