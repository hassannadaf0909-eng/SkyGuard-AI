import pandas as pd

print("====================================")
print("SKYGUARD AI - ANOMALY CLASSIFICATION")
print("====================================")

# Load anomaly results
input_file = "data/processed/anomaly_results.csv"

data = pd.read_csv(input_file)

print()
print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)


# Function to identify anomaly type
def classify_anomaly(row):

    # Only classify detected anomalies
    if row["predicted_anomaly"] == 0:
        return "Normal"

    temperature = row["temperature"]
    pressure = row["pressure"]
    humidity = row["humidity"]

    # Temperature anomaly
    if temperature > 45:
        return "Temperature Spike"

    # Frozen temperature sensor
    if temperature == 0:
        return "Frozen Temperature Sensor"

    # Humidity anomaly
    if humidity < 15:
        return "Humidity Error"

    # Pressure anomaly
    if pressure > 1030 or pressure < 950:
        return "Pressure Error"

    # Unknown anomaly
    return "Unknown Anomaly"


# Apply classification
data["anomaly_type"] = data.apply(
    classify_anomaly,
    axis=1
)


# Save classified results
output_file = "data/processed/classified_anomalies.csv"

data.to_csv(output_file, index=False)


print()
print("Anomaly classification completed!")

print()
print("Anomaly types:")
print(data["anomaly_type"].value_counts())

print()
print("Results saved to:")
print(output_file)

print()
print("====================================")
print("STEP 6 COMPLETED")
print("====================================")