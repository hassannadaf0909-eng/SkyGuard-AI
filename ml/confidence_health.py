import pandas as pd
import numpy as np

print("====================================")
print("SKYGUARD AI - CONFIDENCE & HEALTH")
print("====================================")

# Load classified anomaly data
input_file = "data/processed/classified_anomalies.csv"

data = pd.read_csv(input_file)

print()
print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)


# ------------------------------------
# Calculate AI confidence
# ------------------------------------

def calculate_confidence(row):

    if row["predicted_anomaly"] == 0:
        return 95.0

    anomaly_type = row["anomaly_type"]

    if anomaly_type == "Temperature Spike":
        return 94.0

    elif anomaly_type == "Frozen Temperature Sensor":
        return 98.0

    elif anomaly_type == "Humidity Error":
        return 92.0

    elif anomaly_type == "Pressure Error":
        return 93.0

    else:
        return 75.0


data["ai_confidence"] = data.apply(
    calculate_confidence,
    axis=1
)


# ------------------------------------
# Calculate Data Health
# ------------------------------------

def calculate_health(row):

    if row["predicted_anomaly"] == 0:
        return 95.0

    anomaly_type = row["anomaly_type"]

    if anomaly_type == "Temperature Spike":
        return 40.0

    elif anomaly_type == "Frozen Temperature Sensor":
        return 25.0

    elif anomaly_type == "Humidity Error":
        return 35.0

    elif anomaly_type == "Pressure Error":
        return 40.0

    else:
        return 60.0


data["data_health"] = data.apply(
    calculate_health,
    axis=1
)


# ------------------------------------
# Health status
# ------------------------------------

def health_status(score):

    if score >= 90:
        return "Healthy"

    elif score >= 70:
        return "Warning"

    else:
        return "Critical"


data["health_status"] = data["data_health"].apply(
    health_status
)


# ------------------------------------
# Save results
# ------------------------------------

output_file = "data/processed/skyguard_health_results.csv"

data.to_csv(
    output_file,
    index=False
)


# ------------------------------------
# Display results
# ------------------------------------

print()
print("Confidence and health calculation completed!")

print()
print("Sample results:")

print(
    data[
        [
            "temperature",
            "pressure",
            "humidity",
            "anomaly_type",
            "ai_confidence",
            "data_health",
            "health_status"
        ]
    ].head(10)
)

print()
print("Health Status:")
print(data["health_status"].value_counts())

print()
print("Results saved to:")
print(output_file)

print()
print("====================================")
print("STEP 7 COMPLETED")
print("====================================")