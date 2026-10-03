import pandas as pd

print("====================================")
print("SKYGUARD AI - RISK ENGINE")
print("====================================")

# Load health results
input_file = "data/processed/skyguard_health_results.csv"

data = pd.read_csv(input_file)

print()
print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)


# ------------------------------------
# Temperature Risk
# ------------------------------------

def temperature_risk(temp):

    if temp >= 45:
        return 80

    elif temp >= 40:
        return 60

    elif temp >= 35:
        return 30

    else:
        return 10


# ------------------------------------
# Humidity Risk
# ------------------------------------

def humidity_risk(humidity):

    if humidity >= 90:
        return 70

    elif humidity >= 80:
        return 50

    elif humidity <= 15:
        return 70

    else:
        return 10


# ------------------------------------
# Pressure Risk
# ------------------------------------

def pressure_risk(pressure):

    if pressure < 950 or pressure > 1030:
        return 70

    elif pressure < 980 or pressure > 1020:
        return 40

    else:
        return 10


# Calculate individual risks

data["temperature_risk"] = data["temperature"].apply(
    temperature_risk
)

data["humidity_risk"] = data["humidity"].apply(
    humidity_risk
)

data["pressure_risk"] = data["pressure"].apply(
    pressure_risk
)


# ------------------------------------
# Overall Weather Risk
# ------------------------------------

data["weather_risk"] = (
    data["temperature_risk"] * 0.35
    + data["humidity_risk"] * 0.30
    + data["pressure_risk"] * 0.35
)


# ------------------------------------
# Safety Score
# ------------------------------------

data["safety_score"] = (
    100 - data["weather_risk"]
)


# Make sure score stays between 0 and 100

data["safety_score"] = data["safety_score"].clip(
    0,
    100
)


# ------------------------------------
# Safety Status
# ------------------------------------

def safety_status(score):

    if score >= 90:
        return "Healthy"

    elif score >= 70:
        return "Warning"

    else:
        return "Critical"


data["safety_status"] = data["safety_score"].apply(
    safety_status
)


# ------------------------------------
# Save results
# ------------------------------------

output_file = "data/processed/risk_results.csv"

data.to_csv(
    output_file,
    index=False
)


# ------------------------------------
# Display results
# ------------------------------------

print()
print("Risk calculation completed!")

print()
print("Sample results:")

print(
    data[
        [
            "temperature",
            "pressure",
            "humidity",
            "weather_risk",
            "safety_score",
            "safety_status"
        ]
    ].head(10)
)

print()
print("Safety Status:")
print(
    data["safety_status"].value_counts()
)

print()
print("Results saved to:")
print(output_file)

print()
print("====================================")
print("STEP 8 COMPLETED")
print("====================================")