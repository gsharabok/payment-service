import logging
import typing
import uuid
from sqlalchemy import Column, String, Numeric, DateTime, Enum, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import datetime
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


METADATA: typing.Final = MetaData()


class Base(DeclarativeBase):
    metadata = METADATA


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    balance = Column(Numeric(10, 2), nullable=False, default=0)
    

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id: Mapped[int] = mapped_column(String(36))
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
