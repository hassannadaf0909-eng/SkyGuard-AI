import pandas as pd
import numpy as np

np.random.seed(42)

num_rows = 10000

timestamps = pd.date_range(
    start="2026-01-01 00:00:00",
    periods=num_rows,
    freq="min"
)

time_index = np.arange(num_rows)

temperature = (
    25
    + 5 * np.sin(2 * np.pi * time_index / 1440)
    + np.random.normal(0, 0.5, num_rows)
)

pressure = (
    1013
    + 3 * np.sin(2 * np.pi * time_index / 5000)
    + np.random.normal(0, 0.8, num_rows)
)

humidity = (
    65
    - 10 * np.sin(2 * np.pi * time_index / 1440)
    + np.random.normal(0, 2, num_rows)
)

humidity = np.clip(humidity, 20, 100)

data = pd.DataFrame({
    "timestamp": timestamps,
    "temperature": temperature,
    "pressure": pressure,
    "humidity": humidity
})

output_file = "data/simulated/weather_data.csv"

data.to_csv(output_file, index=False)

print("====================================")
print("SKYGUARD AI DATA GENERATOR")
print("====================================")
print()
print("Dataset generated successfully!")
print("Number of rows:", len(data))
print("Saved to:", output_file)
print()
print(data.head())
