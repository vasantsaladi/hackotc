import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="HackOTC", layout="wide")

# Custom CSS to improve the look
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .main .block-container {
        padding-top: 2rem;
    }
    h1 {
        color: #1E3A8A;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("HackOTC - Forex Business Intelligence")

# Sample data
@st.cache_data
def load_data():
    data = {
        'Country': ['United States', 'United Kingdom', 'Japan', 'Germany', 'France'],
        'Currency': ['USD', 'GBP', 'JPY', 'EUR', 'EUR'],
        'Exchange Rate': [1.0, 0.72, 110.2, 0.84, 0.84],
        'Trade Volume': [1000, 750, 890, 680, 620]
    }
    return pd.DataFrame(data)

df = load_data()

# Sidebar
st.sidebar.header("Country Selection")
selected_countries = st.sidebar.multiselect(
    "Choose countries",
    options=df['Country'].tolist(),
    default=df['Country'].tolist()
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

# Footer
st.markdown("---")
st.markdown("HackOTC - Forex Business Intelligence Dashboard")