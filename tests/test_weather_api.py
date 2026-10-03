import os

from backend.weather_api import get_weather


def test_get_weather_falls_back_when_api_key_missing(monkeypatch):
    monkeypatch.delenv('OPENWEATHER_API_KEY', raising=False)

    result = get_weather('Bengaluru')

    assert isinstance(result, dict)
    assert result['city'] == 'Bengaluru'
    assert 'temperature' in result
    assert 'pressure' in result
    assert 'humidity' in result
    assert 'wind_speed' in result
    assert 'visibility' in result
    assert 'cloud' in result
    assert 'description' in result
