import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables
load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

# Select your database and collection
db = client['Forex_Countries']
collection = db['Countries']

result = collection.delete_many({})
print(f"Deleted {result.deleted_count} documents from the collection.")

client.close()