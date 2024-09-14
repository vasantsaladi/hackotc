import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Data Analysis", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('gdp.csv')
    st.write("Columns in the CSV file:", df.columns.tolist())
    st.write("First few rows of the data:")
    st.write(df.head())
    
    # Attempt to identify appropriate columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    if len(numeric_cols) > 0:
        value_col = numeric_cols[0]
        df = df.rename(columns={value_col: 'VALUE'})
        return df
    else:
        st.error("Unable to identify appropriate numeric column.")
        return None

# Load the data
data = load_data()

if data is not None:
    # Title
    st.title("Data Analysis")

    # Display raw data
    st.subheader("Raw Data")
    st.dataframe(data)

    # Value Distribution
    st.subheader("Value Distribution")
    fig_dist = px.histogram(data, x='VALUE', nbins=50, title='Distribution of Values')
    st.plotly_chart(fig_dist, use_container_width=True)

    # Statistics
    st.subheader("Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Value", f"{data['VALUE'].mean():.2f}")
    col2.metric("Highest Value", f"{data['VALUE'].max():.2f}")
    col3.metric("Lowest Value", f"{data['VALUE'].min():.2f}")

    # Top 10 Values
    st.subheader("Top 10 Values")
    top_10 = data.nlargest(10, 'VALUE')
    fig_top_10 = px.bar(top_10, x=top_10.index, y='VALUE', title='Top 10 Values')
    st.plotly_chart(fig_top_10, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("Data source: gdp.csv")
else:
    st.error("Unable to process the data. Please check your CSV file.")