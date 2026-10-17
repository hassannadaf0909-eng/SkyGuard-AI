from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get('/')

    assert response.status_code == 200
    payload = response.json()
    assert payload['project'] == 'SkyGuard AI'
    assert payload['status'] == 'Backend running'


def test_weather_endpoint_returns_expected_shape():
    response = client.get('/weather?city=Bengaluru')

    assert response.status_code == 200
    payload = response.json()
    assert payload['city'] == 'Bengaluru'
    assert set(payload.keys()) == {'city', 'weather', 'skyguard', 'safety'}
    assert 'temperature' in payload['weather']
    assert 'score' in payload['skyguard']
    assert 'risk' in payload['safety']


def test_route_risk_endpoint_returns_valid_risk_data():
    response = client.get('/route-risk?temperature=30&humidity=70&pressure=1010&rain_probability=10&flood_risk=5&visibility=7')

    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] in {'Healthy', 'Warning', 'Critical'}
    assert 'risk' in payload
    assert 'safety_score' in payload
    assert 'metrics' in payload
