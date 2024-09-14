from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import wbgapi as wb
from datetime import datetime

uri = "mongodb+srv://nagendrashivasaikanneboina:oeHZbmdmfHLvcZK5@hackotc.xbcw3.mongodb.net/?retryWrites=true&w=majority&appName=hackotc"
client = MongoClient(uri, server_api=ServerApi('1'))

# Select your database
db = client['Forex_Countries']

# Select your collection
collection = db['Countries']

# List of countries
countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria",
    "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
    "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
    "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Democratic Republic)",
    "Congo (Republic)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia (Czech Republic)", "Denmark", "Djibouti", "Dominica",
    "Dominican Republic", "East Timor (Timor-Leste)", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia",
    "Eswatini (Swaziland)", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece",
    "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia",
    "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea (North)",
    "Korea (South)", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania",
    "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius",
    "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (Burma)", "Namibia",
    "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan",
    "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia",
    "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
    "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
    "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan",
    "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu",
    "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City",
    "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

# Indicators
indicators = {
    "gdp": "NY.GDP.MKTP.CD",
    "inflation": "FP.CPI.TOTL.ZG",
    "poverty_rate": "SI.POV.DDAY",
    "interest_rate": "FR.INR.RINR",
    "trade_balance": "NE.RSB.GNFS.CD",
    "government_debt": "GC.DOD.TOTL.GD.ZS"
}

def create_country_code_mapping():
    mapping = {}
    for country in wb.economy.list():
        mapping[country['name'].lower()] = country['id']
    return mapping

def fetch_data(indicator, years):
    data = wb.data.fetch(indicator, time=years)
    result = {}
    for d in data:
        economy = d['economy']
        time = d['time']
        value = d['value']
        if value is not None:
            if economy not in result:
                result[economy] = {}
            result[economy][time] = value
    return result

def create_country_documents():
    current_year = datetime.now().year
    years = list(range(current_year - 10, current_year + 1))

    # Fetch data for all indicators
    data = {key: fetch_data(indicator, years) for key, indicator in indicators.items()}

    # Create country code mapping
    country_mapping = create_country_code_mapping()

    for country_name in countries:
        country_code = country_mapping.get(country_name.lower())
        if not country_code:
            print(f"Country code not found for {country_name}")
            continue

        doc = {
            "name": country_name,
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
