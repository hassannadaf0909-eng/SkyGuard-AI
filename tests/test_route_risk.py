from backend.route_engine import calculate_route_risk


def test_calculate_route_risk_returns_healthy_status_for_safe_conditions():
    result = calculate_route_risk(
        temperature=24,
        humidity=55,
        pressure=1013,
        rain_probability=5,
        flood_risk=2,
        visibility=8
    )

    assert result["status"] == "Healthy"
    assert result["risk"] < 20
    assert result["safety_score"] > 80
    assert result["metrics"]["temperature"] == 10
    assert result["metrics"]["visibility"] == 10


def test_calculate_route_risk_returns_critical_status_for_extreme_conditions():
    result = calculate_route_risk(
        temperature=48,
        humidity=93,
        pressure=940,
        rain_probability=90,
        flood_risk=80,
        visibility=0.5
    )

    assert result["status"] == "Critical"
    assert result["risk"] >= 80
    assert result["safety_score"] <= 20
    assert result["metrics"]["rain"] == 90
    assert result["metrics"]["flood"] == 80
