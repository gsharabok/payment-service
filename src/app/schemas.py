from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from datetime import datetime, timezone
from uuid import UUID

class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User(Base):
    id: str
    name: str
    balance: Decimal


class UserCreate(Base):
    id: str
    name: str


class UserBalance(BaseModel):
    balance: Decimal = Field(..., description="The current balance of the user")

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class TransactionAdd(BaseModel):
    user_id: str = Field(..., description="The ID of the user associated with this transaction")
    amount: Decimal = Field(..., description="The amount of the transaction")
    description: str = Field(..., description="A description of the transaction")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="The timestamp of the transaction")

    class Config:
        json_encoders = {
            UUID: str,
            Decimal: float,
            datetime: lambda v: v.isoformat()
        }

class Transaction(BaseModel):
    id: UUID = Field(..., description="The unique identifier for the transaction")
    user_id: str = Field(..., description="The ID of the user associated with this transaction")
    amount: Decimal = Field(..., description="The amount of the transaction")
    description: str = Field(..., description="A description of the transaction")
    timestamp: datetime = Field(..., description="The timestamp of the transaction")

    class Config:
        json_encoders = {
            UUID: str,
            Decimal: float,
            datetime: lambda v: v.isoformat()
        }
