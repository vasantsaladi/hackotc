import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Read the CSV file
df = pd.read_csv('data/wbgdp.csv', index_col='Country Name')

# Select a specific country for analysis (e.g., 'Aruba')
country_data = df.loc['Aruba'].dropna()

# Convert year columns to numeric and drop non-numeric columns
year_columns = [col for col in country_data.index if col.isdigit()]
data = country_data[year_columns].astype(float).values.reshape(-1, 1)

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Prepare data for LSTM
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

seq_length = 5
X, y = create_sequences(scaled_data, seq_length)

# Split data into train and test sets
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Build LSTM model
model = Sequential([
    LSTM(50, activation='relu', input_shape=(seq_length, 1)),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')

# Train the model
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.1, verbose=0)

# Make predictions
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# Inverse transform predictions
train_predict = scaler.inverse_transform(train_predict)
y_train = scaler.inverse_transform(y_train)
test_predict = scaler.inverse_transform(test_predict)
y_test = scaler.inverse_transform(y_test)

# Create a plot
plt.figure(figsize=(12, 6))
plt.plot(year_columns[seq_length:], scaler.inverse_transform(scaled_data[seq_length:]), label='Actual')
plt.plot(year_columns[seq_length:train_size], train_predict, label='Train Predict')
plt.plot(year_columns[train_size+seq_length:], test_predict, label='Test Predict')
plt.title('LSTM Time Series Prediction for Aruba')
plt.xlabel('Year')
plt.ylabel('Value')
plt.legend()
plt.savefig('lstm_prediction_plot.png')
plt.close()

# Create a new CSV file with predictions
results_df = pd.DataFrame({
    'Year': year_columns[seq_length:],
    'Actual': scaler.inverse_transform(scaled_data[seq_length:]).flatten(),
    'Predicted': np.concatenate([train_predict.flatten(), test_predict.flatten()])
})
results_df.to_csv('lstm_predictions.csv', index=False)