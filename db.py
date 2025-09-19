from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

#Connect to Mongo Atlas Cluster
mongo_client = MongoClient(os.getenv("MONGO_URI"))


# Access database
advert_management_db = mongo_client["advert_management_db"]


# Pick a connection to operate on
adverts_collection = advert_management_db["adverts"]
users_collection = advert_management_db["users"]
