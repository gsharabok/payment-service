from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession as AsyncSessionType,
)

from src.app.settings import Settings
from src.app.repositories import PaymentRepository
# from src.app.db.resource import create_session


def get_settings() -> Settings:
    raise NotImplementedError


def get_db() -> async_sessionmaker[AsyncSessionType]:
    raise NotImplementedError


def get_payment_repo(
    db: async_sessionmaker[AsyncSessionType] = Depends(get_db),
) -> PaymentRepository:
    return PaymentRepository(
        db_session_maker=db,
    )
