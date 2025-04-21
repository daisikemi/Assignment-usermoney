from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

try:
    mongo_uri = os.getenv("MONGO_DB_CONNECTION_UR")  # Make sure to set the URI in your .env file
    client = MongoClient(mongo_uri)
    # Access a test database
    db = client.test_database

    # Check if the connection is successful
    print("Connected to MongoDB")
except Exception as e:
    print("Error connecting to MongoDB:", e)