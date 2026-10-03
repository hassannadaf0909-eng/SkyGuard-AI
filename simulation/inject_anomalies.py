import pandas as pd
import numpy as np

# Load normal weather data
input_file = "data/simulated/weather_data.csv"

data = pd.read_csv(input_file)

# Create anomaly column
data["anomaly"] = 0
data["anomaly_type"] = "normal"

np.random.seed(42)

# --------------------------------
# 1. Temperature Spike Anomalies
# --------------------------------

temperature_indices = np.random.choice(
    data.index,
    size=100,
    replace=False
)

data.loc[temperature_indices, "temperature"] += np.random.uniform(
    15, 25, size=100
)

data.loc[temperature_indices, "anomaly"] = 1
data.loc[temperature_indices, "anomaly_type"] = "temperature_spike"


# --------------------------------
# 2. Frozen Sensor Anomalies
# --------------------------------

frozen_start = 3000
frozen_end = 3050

frozen_temperature = data.loc[
    frozen_start, "temperature"
]

data.loc[
    frozen_start:frozen_end,
    "temperature"
] = frozen_temperature

data.loc[
    frozen_start:frozen_end,
    "anomaly"
] = 1

data.loc[
    frozen_start:frozen_end,
    "anomaly_type"
] = "frozen_temperature"


# --------------------------------
# 3. Humidity Anomalies
# --------------------------------

humidity_indices = np.random.choice(
    data.index,
    size=100,
    replace=False
)

data.loc[
    humidity_indices,
    "humidity"
] = np.random.uniform(0, 10, size=100)

data.loc[
    humidity_indices,
    "anomaly"
] = 1

data.loc[
    humidity_indices,
    "anomaly_type"
] = "humidity_error"


# --------------------------------
# 4. Pressure Anomalies
# --------------------------------

pressure_indices = np.random.choice(
    data.index,
    size=100,
    replace=False
)

data.loc[
    pressure_indices,
    "pressure"
] += np.random.uniform(
    20, 40, size=100
)

data.loc[
    pressure_indices,
    "anomaly"
] = 1

data.loc[
    pressure_indices,
    "anomaly_type"
] = "pressure_error"


# --------------------------------
# Save Anomaly Dataset
# --------------------------------

output_file = "data/simulated/weather_data_with_anomalies.csv"

data.to_csv(
    output_file,
    index=False
)

print("====================================")
print("SKYGUARD AI - ANOMALY GENERATOR")
print("====================================")

print()
print("Original records:", len(data))
print("Anomalous records:", data["anomaly"].sum())
print()

print("Anomaly types:")
print(data["anomaly_type"].value_counts())

print()
print("Saved to:")
print(output_file)