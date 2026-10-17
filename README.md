# SkyGuard AI

SkyGuard AI is a weather intelligence dashboard that combines live weather data, SkyGuard anomaly analysis, and route safety scoring into a single web app.

## Features

- Live weather retrieval with simulated fallback data
- AI-style SkyGuard health and anomaly scoring
- Route risk calculation based on temperature, humidity, pressure, visibility, rain, and flood risk
- Minimal frontend dashboard for local monitoring

## Project structure

- `backend/` — FastAPI app and core logic
- `frontend/` — static dashboard UI
- `ml/` — model and analysis utilities
- `tests/` — pytest coverage for backend logic and API routes
- `data/` — raw, processed, and simulated datasets

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your OpenWeather API key:

   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```

   A sample is available in `.env.example`.

4. Start the backend:

   ```powershell
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

5. Start the frontend from the `frontend` folder:

   ```powershell
   cd frontend
   python -m http.server 8001
   ```

6. Open the UI in a browser:

   ```text
   http://localhost:8001/
   ```

## API endpoints

- `GET /` — health check
- `GET /weather?city=Bengaluru` — weather + SkyGuard analysis
- `GET /route-risk?temperature=30&humidity=70&pressure=1010&rain_probability=10&flood_risk=5&visibility=7` — route risk calculation

## Running tests

```powershell
python -m pytest -q
```

## Notes

- If the OpenWeather API key is not configured, the app automatically falls back to simulated weather data.
- The frontend is intentionally lightweight for local demonstration and testing.
