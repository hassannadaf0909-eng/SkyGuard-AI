import csv
import os
from pathlib import Path

import requests

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    def load_dotenv(*args, **kwargs):
        return False


load_dotenv(Path(__file__).resolve().parents[1] / '.env')


# --------------------------------
# WEATHER API CONFIGURATION
# --------------------------------

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
SIMULATED_WEATHER_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "simulated"
    / "weather_data.csv"
)


# --------------------------------
# FALLBACK WEATHER DATA
# --------------------------------

def _get_weather_description(temperature, humidity):
    if humidity >= 85:
        return "humid and cloudy"
    if temperature >= 33:
        return "hot and sunny"
    if temperature <= 10:
        return "cold and clear"
    if 20 <= temperature <= 28:
        return "mild and pleasant"
    return "partly cloudy"


def _load_simulated_weather(city="Bengaluru"):
    try:
        with SIMULATED_WEATHER_PATH.open("r", newline="") as csv_file:
            rows = list(csv.DictReader(csv_file))
    except (FileNotFoundError, OSError):
        rows = []

    if rows:
        row = rows[-1]
        temperature = float(row["temperature"])
        pressure = float(row["pressure"])
        humidity = float(row["humidity"])
    else:
        temperature = 25.0
        pressure = 1013.0
        humidity = 65.0

    return {
        "city": city,
        "temperature": round(temperature, 1),
        "pressure": round(pressure, 1),
        "humidity": round(humidity, 1),
        "wind_speed": round(max(2.0, min(30.0, humidity * 0.35)), 1),
        "visibility": 9.8,
        "cloud": int(min(max(10, humidity), 90)),
        "description": _get_weather_description(temperature, humidity),
        "timestamp": None,
    }


# --------------------------------
# GET LIVE WEATHER
# --------------------------------

def get_weather(city="Bengaluru"):
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if api_key:
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }

        try:
            response = requests.get(
                BASE_URL,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError):
            return _load_simulated_weather(city)

        temperature = data["main"]["temp"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]

        wind_speed = data["wind"].get("speed", 0)
        visibility = data.get("visibility", 10000) / 1000

        cloud = data.get("clouds", {}).get("all", 0)
        description = data["weather"][0]["description"]

        return {
            "city": data.get("name", city),
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humidity,
            "wind_speed": round(wind_speed * 3.6, 1),
            "visibility": round(visibility, 1),
            "cloud": cloud,
            "description": description,
            "timestamp": data.get("dt")
        }

    return _load_simulated_weather(city)