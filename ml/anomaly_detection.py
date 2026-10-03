import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix

print("====================================")
print("SKYGUARD AI - ANOMALY DETECTION")
print("====================================")

# Load dataset
input_file = "data/simulated/weather_data_with_anomalies.csv"

data = pd.read_csv(input_file)

print()
print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)

# Select sensor features
features = [
    "temperature",
    "pressure",
    "humidity"
]

X = data[features]

# Handle missing values
X = X.fillna(X.median())

# Standardize data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print()
print("Sensor data standardized successfully!")

# Create Isolation Forest model
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

# Train model
model.fit(X_scaled)

print()
print("Isolation Forest model trained successfully!")

# Predict anomalies
predictions = model.predict(X_scaled)

# Convert:
# -1 = anomaly
#  1 = normal

data["predicted_anomaly"] = predictions

# Convert to 0/1 format
data["predicted_anomaly"] = data["predicted_anomaly"].apply(
    lambda x: 1 if x == -1 else 0
)

# Save results
output_file = "data/processed/anomaly_results.csv"

data.to_csv(output_file, index=False)

print()
print("Anomaly detection completed!")

print()
print("Detected anomalies:")
print(data["predicted_anomaly"].value_counts())

# Compare with known anomalies
if "anomaly" in data.columns:

    print()
    print("====================================")
    print("MODEL EVALUATION")
    print("====================================")

    print()
    print("Confusion Matrix:")
    print(confusion_matrix(
        data["anomaly"],
        data["predicted_anomaly"]
    ))

    print()
    print("Classification Report:")
    print(classification_report(
        data["anomaly"],
        data["predicted_anomaly"],
        zero_division=0
    ))

print()
print("Results saved to:")
print(output_file)

print()
print("====================================")
print("STEP 5 COMPLETED")
print("====================================")