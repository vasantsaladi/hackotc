import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB connection string from environment variable
mongo_uri = os.getenv('MONGO_URI')

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client['hackathon_db']
collection = db['country_gdp']

# Read CSV file
df = pd.read_csv('data/API_NY/country_gdp.csv', skiprows=4)

# Melt the dataframe to convert years to a single column
df_melted = df.melt(id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
                    var_name='Year', value_name='GDP')

# Convert to dictionary for MongoDB insert
data = df_melted.to_dict('records')

# Insert data into MongoDB
collection.insert_many(data)

print("Data imported successfully!")