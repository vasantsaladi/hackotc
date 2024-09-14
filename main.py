import streamlit as st
import pandas as pd
import csv

# Set page config
st.set_page_config(page_title="Country GDP Data", layout="wide")

# Title
st.title("Country GDP Data")

# Load GDP CSV data
@st.cache_data
def load_gdp_data():
    try:
        # Read the CSV file using csv module
        with open("data/API_NY/country_gdp.csv", 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)
        
        # Display the first few rows to inspect the data
        st.subheader("First few rows of the data:")
        for row in data[:5]:
            st.write(row)
        
        # Ask user to input the number of header rows
        header_rows = st.number_input("Enter the number of header rows:", min_value=0, value=1, step=1)
        
        # Create DataFrame
        df = pd.DataFrame(data[header_rows:], columns=data[header_rows-1] if header_rows > 0 else None)
        
        return df
    except FileNotFoundError:
        st.error("country_gdp.csv not found. Please make sure the file exists in the data/API_NY/ directory.")
        return pd.DataFrame()

df_gdp = load_gdp_data()

if df_gdp.empty:
    st.stop()

# Display the data as a table
st.subheader("GDP Data Table")
st.dataframe(df_gdp)

# Footer
st.markdown("---")
st.markdown("Country GDP Data Dashboard")