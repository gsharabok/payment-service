from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession as AsyncSessionType,
)
from sqlalchemy import insert, select, update, func
from src.app import schemas
from src.app.models import User, Transaction
from datetime import datetime


class PaymentRepository:

    def __init__(self, db_session_maker: async_sessionmaker[AsyncSessionType]):
        self.db_session_maker = db_session_maker

    async def create_user(self, data: schemas.UserCreate) -> User:
        async with self.db_session_maker() as session:
            query = insert(User).values(**data.model_dump()).returning(User)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()
        
    async def get_user_balance(self, user_id: str, ts: datetime = None) -> float:
        async with self.db_session_maker() as session:
            if ts is None:
                # Get current balance
                query = select(User.balance).where(User.id == user_id)
                result = await session.execute(query)
                balance = result.scalar_one_or_none()
                if balance is None:
                    raise ValueError("User not found")
                return float(balance)
            else:
                # Calculate balance at the given timestamp
                query = select(func.coalesce(func.sum(Transaction.amount), 0)).where(
                    Transaction.user_id == user_id,
                    Transaction.timestamp <= ts
                )

                result = await session.execute(query)
                balance = result.scalar_one_or_none()
                if balance is None:
                    raise ValueError("User not found")
                return balance

    async def add_transaction(self, data: schemas.TransactionAdd) -> Transaction:
        async with self.db_session_maker() as session:
            # Update transactions
            query = insert(Transaction).values(**data.model_dump()).returning(Transaction)
            result = await session.execute(query)

            # Update user balance
            query = update(User).where(User.id == data.user_id).values(balance=User.balance + data.amount)
            await session.execute(query)

            await session.commit()
            return result.scalar_one()
        
    async def get_transaction(self, transaction_id: str) -> Transaction:
        async with self.db_session_maker() as session:
            query = select(Transaction).where(Transaction.id == transaction_id)
            result = await session.execute(query)
            return result.scalar_one()
        
    
