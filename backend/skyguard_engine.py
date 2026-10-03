def analyze_sensor_data(temperature, pressure, humidity):
    """
    SkyGuard AI sensor anomaly analysis.

    Inputs:
        temperature -> Celsius
        pressure    -> hPa
        humidity    -> %

    Returns data required by the frontend.
    """

    anomaly_score = 10
    confidence = 95

    reasons = []
    patterns = []
    corrections = []

    # -----------------------------
    # TEMPERATURE CHECK
    # -----------------------------
    if temperature >= 45:
        anomaly_score = max(anomaly_score, 80)
        confidence = 94

        reasons.append("Unusually high temperature detected.")
        patterns.append("Temperature is outside the expected observation range.")

        corrected_temperature = 30.0

    elif temperature <= -10:
        anomaly_score = max(anomaly_score, 75)
        confidence = 92

        reasons.append("Unusually low temperature detected.")
        patterns.append("Temperature differs strongly from normal atmospheric conditions.")

        corrected_temperature = 25.0

    else:
        corrected_temperature = temperature


    # -----------------------------
    # HUMIDITY CHECK
    # -----------------------------
    if humidity <= 15:
        anomaly_score = max(anomaly_score, 75)
        confidence = min(confidence, 92)

        reasons.append("Very low humidity detected.")
        patterns.append("Humidity value may indicate a sensor reading error.")

        corrected_humidity = 60.0

    elif humidity >= 98:
        anomaly_score = max(anomaly_score, 65)
        confidence = min(confidence, 90)

        reasons.append("Extremely high humidity detected.")
        patterns.append("Humidity is near saturation.")

        corrected_humidity = 90.0

    else:
        corrected_humidity = humidity


    # -----------------------------
    # PRESSURE CHECK
    # -----------------------------
    if pressure < 950 or pressure > 1030:
        anomaly_score = max(anomaly_score, 75)
        confidence = min(confidence, 93)

        reasons.append("Atmospheric pressure is outside the expected range.")
        patterns.append("Pressure observation is inconsistent with the expected pattern.")

        corrected_pressure = 1013.25

    else:
        corrected_pressure = pressure


    # -----------------------------
    # FINAL HEALTH
    # -----------------------------
    if anomaly_score >= 70:
        health = "Critical"
        severity = "High"

    elif anomaly_score >= 40:
        health = "Warning"
        severity = "Medium"

    else:
        health = "Healthy"
        severity = "Low"


    # -----------------------------
    # NORMAL OBSERVATION
    # -----------------------------
    if not reasons:
        reasons.append(
            "Temperature, pressure and humidity are within the expected range."
        )

        patterns.append(
            "Observation is consistent with the current sensor pattern."
        )

        correction = "No correction required."

    else:
        correction = (
            f"Suggested values: "
            f"{corrected_temperature:.1f} °C, "
            f"{corrected_pressure:.1f} hPa, "
            f"{corrected_humidity:.1f} %"
        )


    return {
        "score": anomaly_score,
        "conf": confidence,
        "health": health,
        "severity": severity,
        "reason": " ".join(reasons),
        "pattern": " ".join(patterns),
        "correction": correction
    }