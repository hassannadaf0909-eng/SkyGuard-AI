# Secrets and Deployment Checklist

Use this checklist before deploying the app to a shared environment.

## Required secrets

### OpenWeather API key

Set this in your deployment environment or secret store:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

### Render deployment secrets

If using GitHub Actions + Render, configure these repository secrets:

- `RENDER_API_KEY`
- `RENDER_SERVICE_ID`

## GitHub Actions

The workflow in `.github/workflows/deploy.yml` will:

1. install dependencies
2. run tests
3. trigger a Render deploy on push to `main`

## Local checks

Run the app health check before launch:

```powershell
python check_status.py
```

## Production recommendations

- Keep API keys out of source control.
- Use environment variables or a proper secret manager.
- Restrict access to deployment credentials.
- Verify the app responds on the public host before sharing it.
