import os
from pymongo import mongo_client
from dotenv import load_dotenv

load_dotenv()

client = mongo_client.MongoClient("MONGO_DB_CONNECTION_URI")
accounts_collection = client["user_money"]["accounts"]
users_collection = client["user_money"]["users"]
transactions_collection = client["user_money"]["transactions"]
