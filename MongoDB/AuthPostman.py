import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from pymongo import MongoClient
from bson import json_util
import json

load_dotenv()

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client['Forex_Countries']
collection = db['Countries']

@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = list(collection.find({}, {'_id': 0}))
    return json.loads(json_util.dumps(countries))

@app.route('/api/country/<name>', methods=['GET'])
def get_country(name):
    country = collection.find_one({'name': name}, {'_id': 0})
    if country:
        return json.loads(json_util.dumps(country))
    return jsonify({"error": "Country not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)