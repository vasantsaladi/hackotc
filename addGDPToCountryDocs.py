import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

# Select your database and collection
db = client['Forex_Countries']
collection = db['Countries']

def create_country_documents():
    for country_name in countries:
        # Example GDP data (you would replace this with real data)
        gdp_data = [
            {"year": 2010, "gdp": 1000000},
            {"year": 2011, "gdp": 1100000},
            {"year": 2012, "gdp": 1200000},
            # ... add more years as needed
        ]
        
        doc = {
            "name": country_name,
            "gdp_data": gdp_data
        }
        
        result = collection.update_one(
            {"name": country_name},
            {"$set": doc},
            upsert=True
        )
        
        if result.upserted_id:
            print(f"Inserted: {country_name}")
        else:
            print(f"Updated: {country_name}")

# Create documents for all countries
create_country_documents()

# Function to plot GDP data for a country
def plot_gdp(country_name):
    country_data = collection.find_one({"name": country_name})
    if country_data and "gdp_data" in country_data:
        years = [data["year"] for data in country_data["gdp_data"]]
        gdp_values = [data["gdp"] for data in country_data["gdp_data"]]
        
        plt.figure(figsize=(10, 6))
        plt.plot(years, gdp_values, marker='o')
        plt.title(f"GDP Growth for {country_name}")
        plt.xlabel("Year")
        plt.ylabel("GDP")
        plt.grid(True)
        plt.show()
    else:
        print(f"No GDP data found for {country_name}")

# Example usage
plot_gdp("United States")

# Close the connection
client.close()

print("Country documents creation and GDP plotting completed.")