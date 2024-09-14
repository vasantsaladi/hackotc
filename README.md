# hackotc
JHU hackathon project

To build a system that gathers information about countries and makes predictions on currency fluctuations based on that data using **MongoDB** for storing data and visualizing it on a web interface, you'll need to go through the following steps:

### 1. **Data Sources**:
   You need reliable financial data on currency movements and country-specific data (GDP, inflation rates, interest rates, etc.). You can pull data from:
   - **Alpha Vantage** (for real-time and historical currency data).
   - **World Bank APIs** (for country-specific economic indicators like GDP, inflation, etc.).
   - **IMF** and **OECD** (for additional macroeconomic data).
   - **News APIs** (for sentiment analysis, which can influence currency movements).

### 2. **FRED data API**:
   - FRED has up to date economical data
   - Use the datasets and generate a .csv file of it
      - The .csv file will be used as an input for the LSTM ML model (see step 4)

### 3. **Preprocessing and Cleaning Data**:
   Clean and preprocess the data to ensure it's ready for analysis. We will use Python `pandas` to handle this process:
   - Normalize currency data to account for time zones or missing data.
   - Normalize country-specific data.
   - Data handled by FRED API with timestamps and labels to allow easy querying.
   - Singular value decomposition to simplify the dataset to be smaller and more manageable.

### 4. **Develop a Machine Learning Model**:
   - Use historical currency data and country-specific data to train a machine learning model that predicts whether a currency will rise or fall.
   - Algorithms to consider:
     - **Time series forecasting**: ARIMA, LSTM, or Prophet models.
        - We will be using LSTM
     - **Classification models**: Random Forest, Gradient Boosting, or XGBoost for predicting whether a currency will rise or fall based on country metrics.
   - `scikit-learn` & `TensorFlow` will be used.

### 5. **MATLAB scripts**:
   Build script based on new .csv generated post step 4:
   - create_forex_gui.csv

### 6. **Visualizing Data on a Website**:
   - Streamlit can be used for easy backend development and simple frontend
   - Example: Display historical exchange rate trends over time and allow users to select countries and view forecasts for the currency.

### 7. **Scoring & Prediction System**:
   Create a custom scoring or probability system based on model predictions:
   - Example: 
     ```json
     {
       "currency": "USD",
       "probability_of_rise": 0.75,
       "score": 85
     }
     ```
   - This score could be based on multiple factors:
     - Recent trends (e.g., positive news, favorable GDP reports).
     - Sentiment analysis from the news.
     - Machine learning model’s forecast based on time series analysis.

### 8. **Deploy the Web Application**:
   - Use cloud services like **Heroku**, **AWS**, or **Azure** to deploy your website.
   - Set up CI/CD pipelines for continuous deployment and testing.

### Stack Summary:
- **Frontend**: React or Vanilla JavaScript + Chart.js / D3.js for visualizing data.
- **Backend**: Streamlit.
- **Database**: FRED for storing and querying economic and financial data.
- **Data Sources**: FRED, Alpha Vantage, World Bank, IMF, news sentiment APIs.
- **ML Frameworks**: scikit-learn, TensorFlow, statsmodels (ARIMA/Prophet) for predictions.

### Next Steps:
Would you like help with setting up any specific part, like collecting data or building the machine learning model?

### Presentation:
https://new.express.adobe.com/id/urn:aaid:sc:VA6C2:5a4792e7-2db5-5496-a8cc-77beae1695e8?invite=true&promoid=Z2G1FQKR&mv=other
