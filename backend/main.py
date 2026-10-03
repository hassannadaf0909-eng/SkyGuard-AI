from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from backend.weather_api import get_weather
from backend.skyguard_engine import analyze_sensor_data
from backend.route_engine import calculate_route_risk


# ==========================================
# SKYGUARD AI BACKEND
# ==========================================

app = FastAPI(
    title="SkyGuard AI",
    description="AI-powered weather and sensor intelligence system",
    version="1.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "project": "SkyGuard AI",

        "status": "Backend running",

        "message": "SkyGuard AI API is working"
    }


# ==========================================
# LIVE WEATHER + SKYGUARD ANALYSIS
# ==========================================

@app.get("/weather")
def weather(city: str = Query("Bengaluru")):

    # Get live weather
    weather_data = get_weather(city)


    # Analyze sensor values
    analysis = analyze_sensor_data(
        weather_data["temperature"],
        weather_data["pressure"],
        weather_data["humidity"]
    )


    # Calculate safety
    risk = calculate_route_risk(
        temperature=weather_data["temperature"],
        humidity=weather_data["humidity"],
        pressure=weather_data["pressure"],
        rain_probability=0,
        flood_risk=0,
        visibility=weather_data["visibility"]
    )


    return {

        # --------------------------
        # LOCATION
        # --------------------------

        "city": weather_data["city"],


        # --------------------------
        # WEATHER
        # --------------------------

        "weather": {

            "temperature":
                weather_data["temperature"],

            "pressure":
                weather_data["pressure"],

            "humidity":
                weather_data["humidity"],

            "wind_speed":
                weather_data["wind_speed"],

            "visibility":
                weather_data["visibility"],

            "cloud":
                weather_data["cloud"],

            "description":
                weather_data["description"]
        },


        # --------------------------
        # SKYGUARD AWS
        # --------------------------

        "skyguard": {

            "temperature":
                weather_data["temperature"],

            "pressure":
                weather_data["pressure"],

            "humidity":
                weather_data["humidity"],

            "score":
                analysis["score"],

            "confidence":
                analysis["conf"],

            "health":
                analysis["health"],

            "severity":
                analysis["severity"],

            "reason":
                analysis["reason"],

            "pattern":
                analysis["pattern"],

            "correction":
                analysis["correction"]
        },


        # --------------------------
        # SAFETY
        # --------------------------

        "safety": {

            "risk":
                risk["risk"],

            "safety_score":
                risk["safety_score"],

            "status":
                risk["status"],

            "metrics":
                risk["metrics"]
        }
    }


# ==========================================
# ROUTE RISK
# ==========================================

@app.get("/route-risk")
def route_risk(
    temperature: float,
    humidity: float,
    pressure: float,
    rain_probability: float = 0,
    flood_risk: float = 0,
    visibility: float = 10
):

    result = calculate_route_risk(

        temperature=temperature,

        humidity=humidity,

        pressure=pressure,

        rain_probability=rain_probability,

        flood_risk=flood_risk,

        visibility=visibility
    )

    return result