import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import wbdata
from datetime import datetime

# Streamlit app
st.title('GDP for Top 50 Countries (2000-2022)')

# Load data
@st.cache_data
def load_data():
    # Get GDP data for all countries
    countries = wbdata.get_country()
    gdp_indicator = "NY.GDP.MKTP.CD"  # World Bank indicator for GDP (current US$)
    
    # Set date range from 2000 to 2022
    data_date = (datetime(2000, 1, 1), datetime(2022, 12, 31))
    
    data = wbdata.get_dataframe({gdp_indicator: "GDP"}, country=countries, data_date=data_date, convert_date=True)
    data = data.reset_index()
    
    # Pivot the data to have countries as columns
    gdp_data = data.pivot(index="date", columns="country", values="GDP")
    
    # Get the most recent GDP values to determine top 50 countries
    latest_gdp = gdp_data.iloc[-1].sort_values(ascending=False)
    top_50_countries = latest_gdp.head(50).index
    
    # Filter for top 50 countries
    top_50_gdp = gdp_data[top_50_countries]
    
    return top_50_gdp

try:
    gdp_data = load_data()

    # Create Plotly chart
    fig = px.line(gdp_data, title='GDP for Top 50 Countries (2000-2022)')
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='GDP (current US$)',
        legend_title='Country'
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Display raw data
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(gdp_data)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.error("Please try refreshing the page. If the error persists, there might be an issue with the data source.")