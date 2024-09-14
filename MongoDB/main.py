import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

# Set page config (This must be the first Streamlit command)
st.set_page_config(page_title="HackOTC", layout="wide")

# MongoDB connection
# It's better to use environment variables for sensitive information
# MONGODB

@st.cache_resource
def init_connection():
    try:
        return MongoClient("mongodb+srv://cvg237:qQ72QkbuQEuXweBC@cluster0.mbtbp.mongodb.net/") # Self host for now
    except Exception as e:
        st.error(f"Failed to connect to MongoDB: {e}")
        return None

client = init_connection()

# Custom CSS to improve the look
st.markdown("""
<style>
    .reportview-container { background: #f0f2f6 }
    .main .block-container { padding-top: 2rem; }
    h1 { color: #1E3A8A; }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("HackOTC - Forex Business Intelligence")

# Load data from MongoDB
@st.cache_data(ttl=600)
def load_data():
    if client is None:
        return pd.DataFrame()
    try:
        db = client.country_gdp  # Replace with your actual database name
        collection = db.csv  # Replace with your actual collection name
        data = list(collection.find({}, {'_id': 0}))  # Exclude MongoDB's _id field
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data available. Please check your database connection.")
# The issue we're having is that we feeding it trash datasets; we need to ensure the 
# csv file is formatted in such a way in that it falls in line with the following else statement
"""else:
    # Sidebar
    st.sidebar.header("Country Selection")
    selected_countries = st.sidebar.multiselect(
        "Choose countries",
        options=df['Country'].unique().tolist(),
        default=df['Country'].unique().tolist()
    )

    # Filter data based on selection
    filtered_df = df[df['Country'].isin(selected_countries)]
    
    # Main content
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Country Data")
        st.dataframe(filtered_df.style.highlight_max(axis=0), use_container_width=True)

    with col2:
        st.subheader("Visualizations")
        
        # Exchange Rate Chart
        fig1 = px.bar(filtered_df, x='Country', y='Exchange Rate', title='Exchange Rates',
                      color='Country', height=300)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Trade Volume Chart
        fig2 = px.scatter(filtered_df, x='Exchange Rate', y='Trade Volume', color='Country',
                          size='Trade Volume', hover_name='Country', title='Trade Volume vs Exchange Rate',
                          height=300)
        st.plotly_chart(fig2, use_container_width=True)

    # Expandable country details
    st.subheader("Country Details")
    for country in selected_countries:
        with st.expander(f"Details for {country}"):
            country_data = filtered_df[filtered_df['Country'] == country].iloc[0]
            st.write(f"Currency: {country_data['Currency']}")
            st.write(f"Exchange Rate: {country_data['Exchange Rate']:.2f}")
            st.write(f"Trade Volume: {country_data['Trade Volume']}")
            
            # Additional visualizations could be added here
            fig = px.pie(names=['Exchange Rate', 'Trade Volume'],
                         values=[country_data['Exchange Rate'], country_data['Trade Volume']],
                         title=f"{country} Metrics")
            st.plotly_chart(fig, use_container_width=True)
"""
# Footer
st.markdown("---")
st.markdown("HackOTC - Forex Business Intelligence Dashboard")