from pymongo import MongoClient

# Connect to the local MongoDB instance
client = MongoClient('mongodb://localhost:27017/')

# Select your database (it will be created if it doesn't exist)
db = client['Forex_Countries']

# Select your collection (it will be created if it doesn't exist)
collection = db['Countries']

# Example: Insert a document
doc = {"name": "John Doe", "age": 30}
result = collection.insert_one(doc)
print(f"Inserted document ID: {result.inserted_id}")

# Example: Find documents
for doc in collection.find():
    print(doc)

# Close the connection
client.close()