def calculate_route_risk(
    temperature,
    humidity,
    pressure,
    rain_probability=0,
    flood_risk=0,
    visibility=10
):

    # -----------------------------
    # TEMPERATURE RISK
    # -----------------------------

    if temperature >= 45:
        temperature_risk = 90
    elif temperature >= 40:
        temperature_risk = 70
    elif temperature >= 35:
        temperature_risk = 40
    else:
        temperature_risk = 10


    # -----------------------------
    # HUMIDITY RISK
    # -----------------------------

    if humidity >= 90:
        humidity_risk = 70
    elif humidity >= 80:
        humidity_risk = 50
    elif humidity <= 15:
        humidity_risk = 70
    else:
        humidity_risk = 10


    # -----------------------------
    # PRESSURE RISK
    # -----------------------------

    if pressure < 950 or pressure > 1030:
        pressure_risk = 70
    elif pressure < 980 or pressure > 1020:
        pressure_risk = 40
    else:
        pressure_risk = 10


    # -----------------------------
    # VISIBILITY RISK
    # -----------------------------

    if visibility < 1:
        visibility_risk = 90
    elif visibility < 3:
        visibility_risk = 60
    elif visibility < 5:
        visibility_risk = 30
    else:
        visibility_risk = 10


    # -----------------------------
    # COMBINED RISK
    # -----------------------------

    weather_risk = (
        temperature_risk * 0.15 +
        humidity_risk * 0.15 +
        pressure_risk * 0.10 +
        rain_probability * 0.25 +
        flood_risk * 0.25 +
        visibility_risk * 0.10
    )

    weather_risk = min(100, max(0, weather_risk))

    safety_score = 100 - weather_risk


    # -----------------------------
    # STATUS
    # -----------------------------

    if safety_score >= 90:
        status = "Healthy"

    elif safety_score >= 70:
        status = "Warning"

    else:
        status = "Critical"


    return {
        "risk": round(weather_risk, 1),
        "safety_score": round(safety_score, 1),
        "status": status,

        "metrics": {
            "temperature": temperature_risk,
            "humidity": humidity_risk,
            "pressure": pressure_risk,
            "rain": rain_probability,
            "flood": flood_risk,
            "visibility": visibility_risk
        }
    }