import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

#client = mongo_client.MongoClient("MONGO_DB_CONNECTION_URI")
mongo_uri = os.getenv("MONGO_DB_CONNECTION_URI")
client = MongoClient(mongo_uri)

accounts_collection = client["user_money"]["accounts"]
users_collection = client["user_money"]["users"]
transactions_collection = client["user_money"]["transactions"]
