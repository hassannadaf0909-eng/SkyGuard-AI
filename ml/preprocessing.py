import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load anomaly dataset
input_file = "data/simulated/weather_data_with_anomalies.csv"

data = pd.read_csv(input_file)

print("====================================")
print("SKYGUARD AI - DATA PREPROCESSING")
print("====================================")

print()
print("Dataset shape:", data.shape)
print()

# Select sensor features
features = [
    "temperature",
    "pressure",
    "humidity"
]

X = data[features]

# Check missing values
print("Missing values:")
print(X.isnull().sum())

# Handle missing values
X = X.fillna(X.median())

# Standardize sensor values
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# Convert back to DataFrame
X_scaled = pd.DataFrame(
    X_scaled,
    columns=features
)

print()
print("Preprocessing completed successfully!")

print()
print("Processed data:")
print(X_scaled.head())

print()
print("Features used:")
print(features)