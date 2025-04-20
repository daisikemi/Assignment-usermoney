from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.account import AccountCreatePayload, AccountCreate, Account
from database import accounts_collection
from schemas.transaction import DepositTransactionPayload, WithdrawTransactionPayload
from schemas.user import User
from serializers import account_serializer 
from bson.objectid import ObjectId


class AccountService:

    @staticmethod
    def create_account(account_data: AccountCreatePayload, user: User) -> Account:
        account_data = account_data.model_dump()
        account_with_defaults = Account(
            **account_data,
            user_id=user.id,
            balance=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        account_id = accounts_collection.insert_one(jsonable_encoder(account_with_defaults)).inserted_id
        account = accounts_collection.find_one({"_id": account_id})
        return account_serializer(account)


    @staticmethod
    def get_account(user: User):
        account = accounts_collection.find_one({"user_id": user.id})
        return account_serializer(account)
    

    @staticmethod
    def get_account_by_id(account_id: str):
        account = accounts_collection.find_one({"_id": ObjectId(account_id)})
        return account_serializer(account)

    @staticmethod
    def deposit_fund(deposit_payload: DepositTransactionPayload, account_id):
        account = AccountService.get_account_by_id(account_id)
        old_balance = float(account.balance)
        new_balance = old_balance + float(deposit_payload.amount)
        account.balance = new_balance
        account = accounts_collection.find_one_and_update(
            {"_id": ObjectId(account.id)},
            {"$set": {"balance": new_balance}}
        )
        return "successful"
    

    @staticmethod
    def get_account_by_id(account_id: str):
        account = accounts_collection.find_one({"_id": ObjectId(account_id)})
        if not account:
            raise HTTPException(status_code=404, detail="Account not found.")
        return account_serializer(account)

    @staticmethod
    def update_account_balance(account_id: str, new_balance: float):
        result = accounts_collection.update_one(
            {"_id": ObjectId(account_id)},
            {"$set": {"balance": new_balance}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Failed to update account balance.")

    @staticmethod
    def withdraw_fund(transaction: WithdrawTransactionPayload, account_id: str, current_user):
        account = AccountService.get_account_by_id(account_id)

        if str(account.user_id) != str(current_user.id):
            raise HTTPException(status_code=403, detail="You do not own this account.")

        if transaction.amount > account.balance:
            raise HTTPException(status_code=400, detail="Insufficient funds.")

        new_balance = float(account.balance - Decimal(transaction.amount))
        AccountService.update_account_balance(account_id, new_balance)

        updated_account = AccountService.get_account_by_id(account_id)

        return {
            "message": "Withdrawal successful",
            "data": updated_account
        }


account_service = AccountService()



account_service = AccountService()
