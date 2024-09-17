import pandas as pd
import plotly.express as px
import streamlit as st

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

# Streamlit app
st.title('Germany GDP: Actual vs Predicted')

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('lstm_predictions.csv')
    st.write("Column names:", df.columns.tolist())
    st.write("First few rows of the data:")
    st.write(df.head())
    return df

gdp_data = load_data()

# Identify the correct columns
year_column = gdp_data.columns[0]  # Assuming Year is the first column
actual_column = gdp_data.columns[1]  # Assuming Actual GDP is the second column
predicted_column = gdp_data.columns[2]  # Assuming Predicted GDP is the third column

# Convert GDP values to billions for better readability
gdp_data[actual_column] = gdp_data[actual_column] / 1e9
gdp_data[predicted_column] = gdp_data[predicted_column] / 1e9

# Create a clean, professional-looking graph using Plotly Express
fig = px.line(gdp_data, x=year_column, y=[actual_column, predicted_column],
              title='Germany GDP: Actual vs Predicted',
              labels={year_column: 'Year', 'value': 'GDP (Billions of Euros)', 'variable': 'Type'},
              color_discrete_map={actual_column: 'blue', predicted_column: 'red'},
              template='plotly_white')

# Customize the layout
fig.update_layout(
    legend_title_text='',
    xaxis_title='Year',
    yaxis_title='GDP (Billions of Euros)',
    hovermode='x unified',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)

# Update line styles
fig.update_traces(line=dict(width=2))

# Improve x-axis formatting
fig.update_xaxes(
    dtick=1,  # Show tick marks for each year
    tickformat='d'  # Display years as integers
)

# Improve y-axis formatting
fig.update_yaxes(
    tickprefix='€',  # Add euro symbol to y-axis values
    tickformat=',.0f'  # Format as thousands with no decimal places
)

# Set y-axis range to start from 0
fig.update_yaxes(range=[0, gdp_data[[actual_column, predicted_column]].max().max() * 1.1])

# ... (previous code remains the same)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Create three columns for metrics
col1, col2, col3 = st.columns(3)

# Calculate and display accuracy metrics
mse = ((gdp_data[actual_column] - gdp_data[predicted_column]) ** 2).mean()
rmse = mse ** 0.5
mae = (gdp_data[actual_column] - gdp_data[predicted_column]).abs().mean()

with col1:
    st.metric(label="Mean Squared Error", value=f"€{mse:.2f}B")

with col2:
    st.metric(label="Root Mean Squared Error", value=f"€{rmse:.2f}B")

with col3:
    st.metric(label="Mean Absolute Error", value=f"€{mae:.2f}B")

# Identify potential recessions
gdp_data['GDP_Change'] = gdp_data[actual_column].pct_change()
recessions = gdp_data[(gdp_data['GDP_Change'] < 0) & (gdp_data['GDP_Change'].shift(1) < 0)]

# Display recession information in an expander
with st.expander("Potential Recession Periods", expanded=True):
    if not recessions.empty:
        st.write("Years with potential recessions:")
        for _, recession in recessions.iterrows():
            st.info(f"**{recession[year_column]}**")
        
        st.write("A recession is identified when there are two consecutive years of negative GDP growth.")
    else:
        st.success("No potential recessions identified based on consecutive negative GDP growth.")

# Add some context about the metrics
st.markdown("""
### Understanding the Metrics

- **Mean Squared Error (MSE)**: Measures the average squared difference between predicted and actual values. Lower values indicate better predictions.
- **Root Mean Squared Error (RMSE)**: The square root of MSE, providing a measure in the same unit as the GDP. Lower values indicate better predictions.
- **Mean Absolute Error (MAE)**: Measures the average absolute difference between predicted and actual values. Lower values indicate better predictions.

These metrics help assess the accuracy of the GDP predictions compared to actual values.
""")