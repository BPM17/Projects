import datetime
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
password = "E0937:1155@"
MONGODB_URI = os.environ[f'mongodb+srv://admin:{password}@myapi.4hayr.mongodb.net/?retryWrites=true&w=majority&appName=MyApi']

client = MongoClient(MONGODB_URI)

for db_info in client.list_database_names():
    print("ok")