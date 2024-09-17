import pandas as pd
import plotly.express as px
import streamlit as st

# Streamlit app
st.title('GDP by Country')

# Load data
@st.cache_data
def load_data():
    # Load the CSV file
    df = pd.read_csv('data/wbgdp.csv')
    
    # Melt the dataframe to convert years to a single column
    df_melted = df.melt(id_vars=['Country Name', 'Country Code'], 
                        var_name='Year', 
                        value_name='GDP')
    
    # Convert Year to datetime
    df_melted['Year'] = pd.to_datetime(df_melted['Year'], format='%Y')
    
    # Drop rows with missing GDP values
    df_melted = df_melted.dropna(subset=['GDP'])
    
    return df_melted

gdp_data = load_data()

# Create Plotly chart
fig = px.line(gdp_data, 
              x='Year', 
              y='GDP', 
              color='Country Name',
              title='GDP by Country Over Time')

# Improve layout
fig.update_layout(
    xaxis_title='Year',
    yaxis_title='GDP (current US$)',
    legend_title='Country'
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)