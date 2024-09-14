import os
import csv
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

# Select your database and collection
db = client['Forex_Countries']
collection = db['Countries']

def load_gdp_data(file_path):
    gdp_data = {}
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)
        years = headers[4:]  # Years start from the 5th column
        for row in csv_reader:
            country_name = row[4]
            country_gdp = []
            for i, gdp in enumerate(row[4:]):
                if gdp:
                    country_gdp.append({"year": int(years[i]), "gdp": float(gdp)})
            gdp_data[country_name] = country_gdp
    return gdp_data

def update_country_documents(gdp_data):
    for country in collection.find():
        country_name = country['name']
        if country_name in gdp_data:
            collection.update_one(
                {"_id": country['_id']},
                {"$set": {"gdp_data": gdp_data[country_name]}}
            )
            print(f"Updated GDP data for {country_name}")

# # Function to plot GDP data for a country
# def plot_gdp(country_name):
#     country_data = collection.find_one({"name": country_name})
#     if country_data and "gdp_data" in country_data:
#         years = [data["year"] for data in country_data["gdp_data"]]
#         gdp_values = [data["gdp"] for data in country_data["gdp_data"]]
        
#         plt.figure(figsize=(10, 6))
#         plt.plot(years, gdp_values, marker='o')
#         plt.title(f"GDP Growth for {country_name}")
#         plt.xlabel("Year")
#         plt.ylabel("GDP (current US$)")
#         plt.grid(True)
#         plt.show()
#     else:
#         print(f"No GDP data found for {country_name}")

# Load GDP data
gdp_data = load_gdp_data('data/API_NY/country_gdp.csv')

# Update country documents with GDP data
update_country_documents(gdp_data)

# Example usage: Plot GDP for a specific country
# plot_gdp("United States")

# Close the connection
client.close()

print("Country documents updated with GDP data and plotting completed.")