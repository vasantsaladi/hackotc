import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from fredapi import Fred
from dotenv import load_dotenv
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load environment variables
load_dotenv()

# Get the FRED API key from the environment variable
fred_api_key = os.getenv('fred_key')

# Initialize FRED with the API key
fred = Fred(api_key=fred_api_key)

# Set up page configuration
st.set_page_config(page_title="Economic Data Visualization", layout="wide")

# Streamlit app title
st.title("Economic Data Visualization")

# Fetch S&P 500 data
@st.cache_data
def get_sp500_data():
    return fred.get_series(series_id='SP500')

sp500 = get_sp500_data()

# Plot S&P 500
st.subheader("S&P 500")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(sp500.index, sp500.values, linewidth=2)
ax.set_title('S&P 500')
st.pyplot(fig)

# Fetch unemployment data
@st.cache_data
def get_unemployment_data():
    unemp_df = fred.search('unemployment rate state', filter=('frequency','Monthly'))
    unemp_df = unemp_df.query('seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"')
    unemp_df = unemp_df.loc[unemp_df['title'].str.contains('Unemployment Rate')]
    
    all_results = []
    for myid in unemp_df.index:
        results = fred.get_series(myid)
        results = results.to_frame(name=myid)
        all_results.append(results)
    
    if not all_results:
        st.error("No unemployment data found. Please check your FRED API key and internet connection.")
        return pd.DataFrame()
    
    uemp_results = pd.concat(all_results, axis=1)
    
    id_to_state = unemp_df['title'].str.replace('Unemployment Rate in ','').to_dict()
    uemp_states = uemp_results.copy()
    uemp_states = uemp_states.dropna()
    uemp_states.columns = [id_to_state[c] for c in uemp_states.columns]
    return uemp_states

uemp_states = get_unemployment_data()

# Check if uemp_states is empty
if uemp_states.empty:
    st.warning("No unemployment data available.")
else:
    # Ensure the index is datetime
    uemp_states.index = pd.to_datetime(uemp_states.index)

    # Plot States Unemployment Rate
    st