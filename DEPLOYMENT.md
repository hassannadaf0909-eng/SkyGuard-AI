# Deployment Guide

This project can run locally with Python, or via Docker Compose for a more isolated setup.

## Local development

1. Activate the virtual environment:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. Start the backend:

   ```powershell
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

3. Start the frontend:

   ```powershell
   cd frontend
   python -m http.server 8001
   ```

4. Open:

   ```text
   http://localhost:8001/
   ```

## Docker Compose

From the project root:

```powershell
docker compose up --build
```

Then access:

- Backend: http://localhost:8000
- Frontend: http://localhost:8001

## Environment variables

Create a `.env` file in the project root with:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

If the key is missing, the app falls back to simulated weather data automatically.

## Production notes

- Use a real secret manager or environment injection service for API keys.
- Keep the frontend static host separate from the API if scaling beyond local development.
- Add HTTPS and reverse-proxy configuration when deploying to a public environment.
