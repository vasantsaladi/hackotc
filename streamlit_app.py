import streamlit as st
import pymongo
import subprocess
import os
import scipy.io

# Initialize connection
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

# Pull data from the collection
@st.cache_data(ttl=600)
def get_data():
    db = client.mydb
    items = db.mycollection.find()
    items = list(items)  # make hashable for st.cache_data
    return items

items = get_data()

# Print results from MongoDB collection
for item in items:
    st.write(f"{item['name']} has a :{item['pet']}:")

# Function to run Octave script
def run_octave_script(script_path):
    command = f'octave --no-gui --silent {script_path}'
    try:
        subprocess.run(command, shell=True, check=True)
        # Load the processed data from the .mat file
        if os.path.exists('processed_data.mat'):
            mat_data = scipy.io.loadmat('processed_data.mat')
            return mat_data.get('forex_data', 'No data found')
        else:
            return "No result file found. There might be an error in the script."
    except subprocess.CalledProcessError as e:
        st.error(f"Error running Octave script: {e}")
        return None

# Button to run the Octave script
if st.button('Run Octave Script'):
    result = run_octave_script('create_forex_data.m')
    if result is not None:
        st.write('Processed Data:')
        st.write(result)
