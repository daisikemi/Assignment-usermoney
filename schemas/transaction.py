from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from enum import Enum


class TransactionType(Enum):
    debit = "debit"
    credit = "credit"


class TransactionBase(BaseModel):
    transaction_type: TransactionType
    amount: Decimal


class DepositTransactionPayload(BaseModel):
    amount: Decimal


class DepositTransaction(BaseModel):
    account_id: str
    amount: Decimal
    transaction_type: str = TransactionType.credit.value
    date: datetime = datetime.now()


# class WithdrawTransaction(T)


class TransactionDb(TransactionBase):
    account_id: str
    date: datetime

class WithdrawTransactionPayload(BaseModel):
    amount: float = Field(..., gt=0, description="Amount to withdraw")
