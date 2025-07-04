import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = f"mongodb+srv://{os.getenv('mongo_username')}:{os.getenv('mongo_password')}@ambar.s07gddt.mongodb.net/?retryWrites=true&w=majority&appName=AmBar"

client = MongoClient(uri)
db = client["Orivo"]
# collection = db["Spam"]

def create(collection_name, document):
    collection = db[collection_name]
    collection.insert_one(document)

def read(collection_name, document):
    collection = db[collection_name]
    collection.find_one(document)

def update(collection_name, document, new):
    collection = db[collection_name]
    collection.update_one(document, new)

def delete(collection_name, document):
    collection = db[collection_name]
    collection.delete_one(document)

if __name__=="__main__":
    create("Spam", 
           {"timestamp": "Alice", 
            "username": 25,
            "message":"",
            "channel":""
            })