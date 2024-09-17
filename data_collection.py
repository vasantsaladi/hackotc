import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

"""Data Collection"""
# RSI = 100 - (100) / (1 + RS)
def calculate_rsi(series, window=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi
Money
"""
Compute the 12-day EMA (Exponential Moving Average) and 26-day EMA.
Subtract the 26-day EMA from the 12-day EMA to get the MACD line.
Compute the 9-day EMA of the MACD line to get the signal line.
"""
def calculate_macd(series):
    ema_12 = series.ewm(span=12, adjust=False).mean()
    ema_26 = series.ewm(span=26, adjust=False).mean()

    macd_line = ema_12 - ema_26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()

    return macd_line, signal_line

# Load and prepare data
df = pd.read_csv('gdp.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Calculate additional features
df['MA5'] = df['Close'].rolling(window=5).mean()
df['MA20'] = df['Close'].rolling(window=20).mean()
df['RSI'] = calculate_rsi(df['Close'], window=14)
df['MACD'] = calculate_macd(df['Close'])

# Feature selection
features = ['Open', 'High', 'Low', 'Close', 'Volume', 'MA5', 'MA20', 'RSI', 'MACD']  # Add RSI & MACD
X = df[features]
y = df['Close'].shift(-1)  # Predict next day's closing price

# Remove rows with NaN values
df = df.dropna()
X = X.loc[df.index]
y = y.loc[df.index]

# Select top k features
k = 5
# X and y must be aligned and contain no NaNs
selector = SelectKBest(score_func=f_regression, k=k)
X_selected = selector.fit_transform(X, y)
selected_features = X.columns[selector.get_support()].tolist()

print(f"Selected features: {selected_features}")

# Prepare data for LSTM
def create_sequences(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        Xs.append(X.iloc[i:(i + time_steps)].values)
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)

time_steps = 60  # Use 60 days of historical data to predict the next day
X_seq, y_seq = create_sequences(X[selected_features], y, time_steps)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2, shuffle=False)

# Scale the features
scaler = StandardScaler()
X_train_reshaped = X_train.reshape(-1, X_train.shape[-1])
X_test_reshaped = X_test.reshape(-1, X_test.shape[-1])
X_train_scaled = scaler.fit_transform(X_train_reshaped).reshape(X_train.shape)
X_test_scaled = scaler.transform(X_test_reshaped).reshape(X_test.shape)

"""Machine learning"""
# Build the LSTM model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(time_steps, len(selected_features))),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
history = model.fit(
    X_train_scaled, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Make predictions
y_pred = model.predict(X_test_scaled)

# Calculate error metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"Root Mean Squared Error: {rmse}")
print(f"Mean Absolute Error: {mae}")

# Plot actual vs predicted prices
plt.figure(figsize=(12, 6))
plt.plot(y_test, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.title('Stock Price Prediction')
plt.show()

# Plot training history
plt.figure(figsize=(12, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.title('Model Training History')
plt.show()

# Evaluate directional accuracy
def directional_accuracy(y_true, y_pred):
    return np.mean((y_true[1:] > y_true[:-1]) == (y_pred[1:] > y_pred[:-1]))

dir_acc = directional_accuracy(y_test, y_pred)
print(f"Directional Accuracy: {dir_acc:.2f}")

# Backtesting (simple example)
initial_balance = 10000
balance = initial_balance
shares = 0

for i in range(1, len(y_test)):
    if y_pred[i] > y_test[i - 1]:  # If we predict price will go up
        if shares == 0:  # Buy if we don't have shares
            shares = balance // y_test[i - 1]
            balance -= shares * y_test[i - 1]
    elif y_pred[i] < y_test[i - 1]:  # If we predict price will go down
        if shares > 0:  # Sell if we have shares
            balance += shares * y_test[i - 1]
            shares = 0

# Final valuation
final_balance = balance + shares * y_test[-1]
returns = (final_balance - initial_balance) / initial_balance * 100

print(f"Initial balance: ${initial_balance}")
print(f"Final balance: ${final_balance:.2f}")
print(f"Return: {returns:.2f}%")
