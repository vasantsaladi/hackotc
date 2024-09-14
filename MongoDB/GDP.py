import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import wbgapi as wb
from datetime import datetime

# Ignore warning messages
import warnings
from urllib3.exceptions import NotOpenSSLWarning

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)



# Load environment variables
load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

# Select your database
db = client['Forex_Countries']

# Select your collection
collection = db['Countries']

# Indicators
indicators = {
    "gdp": "NY.GDP.MKTP.CD",
    "inflation": "FP.CPI.TOTL.ZG",
    "poverty_rate": "SI.POV.DDAY",
    "interest_rate": "FR.INR.RINR",
    "trade_balance": "NE.RSB.GNFS.CD",
    "government_debt": "GC.DOD.TOTL.GD.ZS"
}

def fetch_data(indicator, years):
    # Fetch data using the provided indicator and years
    data = wb.data.fetch(indicator, time=years)
    
    # Initialize the result dictionary
    result = {}
    
    # Process each data entry
    for d in data:
        economy = d['economy']
        time = d['time']
        value = d['value']
        
        # Only process if value is not None
        if value is not None:
            # Initialize the economy entry if not already present
            if economy not in result:
                result[economy] = {}
            
            # Assign the value to the appropriate time
            result[economy][time] = value
    
    # Return the processed result
    return result


from datetime import datetime

def create_country_documents():
    current_year = datetime.now().year
    years = list(range(current_year - 100, current_year + 1))

    # Fetch data for all indicators
    data = {key: fetch_data(indicator, years) for key, indicator in indicators.items()}

    # Iterate over country documents in the collection
    for country_doc in collection.find({}, {'name': 1, 'alpha3code': 1}):
        country_name = country_doc['name']
        country_code = country_doc['alpha3code']
        
        if not country_code:
            print(f"Country code not found for {country_name}")
            continue

        # Create the document structure
        doc = {
            "name": country_name,
            "alpha3code": country_code,
            "economic_indicators": {
                str(year): {
                    "gdp": data["gdp"].get(country_code, {}).get(str(year)),
                    "inflation": data["inflation"].get(country_code, {}).get(str(year)),
                    "poverty_rate": data["poverty_rate"].get(country_code, {}).get(str(year)),
                    "interest_rate": data["interest_rate"].get(country_code, {}).get(str(year)),
                    "trade_balance": data["trade_balance"].get(country_code, {}).get(str(year)),
                    "government_debt": data["government_debt"].get(country_code, {}).get(str(year))
                } for year in years
            }
        }
    
        # Update or insert the document in the collection
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

# Close the connection
client.close()

print("Country documents creation completed.")
