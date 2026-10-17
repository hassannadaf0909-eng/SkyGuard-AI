const API_BASE = 'http://127.0.0.1:8002';

const weatherGrid = document.getElementById('weather-grid');
const weatherStatus = document.getElementById('weather-status');
const skyguardScore = document.getElementById('skyguard-score');
const skyguardDetails = document.getElementById('skyguard-details');
const safetyScore = document.getElementById('safety-score');
const safetyDetails = document.getElementById('safety-details');
const cityForm = document.getElementById('city-form');
const cityInput = document.getElementById('city-input');
const routeForm = document.getElementById('route-form');
const routeStatus = document.getElementById('route-status');
const routeDetails = document.getElementById('route-details');
const historyChart = document.getElementById('history-chart');

function createMetric(label, value) {
  const el = document.createElement('div');
  el.className = 'metric';
  el.innerHTML = `
    <label>${label}</label>
    <strong>${value}</strong>
  `;
  return el;
}

function createInfoRow(label, value) {
  const el = document.createElement('div');
  el.className = 'info-row';
  el.innerHTML = `
    <label>${label}</label>
    <span>${value}</span>
  `;
  return el;
}

function renderWeather(data) {
  const weather = data.weather || {};
  const city = data.city || 'Unknown';

  weatherStatus.textContent = `${city} • ${weather.description || 'Weather report'}`;
  weatherGrid.innerHTML = '';

  const metrics = [
    ['Temperature', `${weather.temperature ?? '--'}°C`],
    ['Humidity', `${weather.humidity ?? '--'}%`],
    ['Pressure', `${weather.pressure ?? '--'} hPa`],
    ['Wind', `${weather.wind_speed ?? '--'} km/h`],
    ['Visibility', `${weather.visibility ?? '--'} km`],
    ['Cloud', `${weather.cloud ?? '--'}%`]
  ];

  metrics.forEach(([label, value]) => {
    weatherGrid.appendChild(createMetric(label, value));
  });
}

function renderSkyguard(data) {
  const skyguard = data.skyguard || {};
  skyguardScore.textContent = `${skyguard.score ?? '--'}`;
  skyguardScore.style.color = skyguard.score >= 70 ? '#5ce1a8' : '#f9d76d';

  skyguardDetails.innerHTML = '';
  const rows = [
    ['Health', skyguard.health || '--'],
    ['Confidence', `${skyguard.confidence ?? '--'}%`],
    ['Severity', skyguard.severity || '--'],
    ['Reason', skyguard.reason || '--'],
    ['Pattern', skyguard.pattern || '--'],
    ['Correction', skyguard.correction || '--']
  ];

  rows.forEach(([label, value]) => {
    skyguardDetails.appendChild(createInfoRow(label, value));
  });
}

function renderSafety(data) {
  const safety = data.safety || {};
  safetyScore.textContent = `${safety.safety_score ?? '--'}`;
  safetyScore.style.color = safety.safety_score >= 70 ? '#5ce1a8' : '#f9d76d';

  safetyDetails.innerHTML = '';
  const rows = [
    ['Risk', `${safety.risk ?? '--'}%`],
    ['Status', safety.status || '--'],
    ['Temperature risk', `${safety.metrics?.temperature ?? '--'}`],
    ['Humidity risk', `${safety.metrics?.humidity ?? '--'}`],
    ['Pressure risk', `${safety.metrics?.pressure ?? '--'}`],
    ['Visibility risk', `${safety.metrics?.visibility ?? '--'}`]
  ];

  rows.forEach(([label, value]) => {
    safetyDetails.appendChild(createInfoRow(label, value));
  });
}

function setRouteDefaults(weather = {}) {
  document.getElementById('temperature').value = weather.temperature ?? 23.6;
  document.getElementById('humidity').value = weather.humidity ?? 68;
  document.getElementById('pressure').value = weather.pressure ?? 1011.7;
  document.getElementById('visibility').value = weather.visibility ?? 9.8;
}

function renderRouteResult(data) {
  const status = data.status || '--';
  const risk = data.risk ?? '--';
  const safetyScoreValue = data.safety_score ?? '--';

  routeStatus.textContent = status;
  routeStatus.style.color = status === 'Healthy' ? '#5ce1a8' : status === 'Warning' ? '#f9d76d' : '#ff7d7d';

  routeDetails.innerHTML = '';
  const rows = [
    ['Risk score', `${risk}%`],
    ['Safety score', `${safetyScoreValue}`],
    ['Temperature component', `${data.metrics?.temperature ?? '--'}`],
    ['Humidity component', `${data.metrics?.humidity ?? '--'}`],
    ['Pressure component', `${data.metrics?.pressure ?? '--'}`],
    ['Visibility component', `${data.metrics?.visibility ?? '--'}`]
  ];

  rows.forEach(([label, value]) => {
    routeDetails.appendChild(createInfoRow(label, value));
  });

  renderHistoryChart(Number(risk || 0));

  renderTrendBars({
    temperature: Number(document.getElementById('temperature').value || 0),
    humidity: Number(document.getElementById('humidity').value || 0),
    visibility: Number(document.getElementById('visibility').value || 0),
    risk: Number(risk || 0)
  });
}

function renderTrendBars(values) {
  const container = document.getElementById('trend-bars');
  if (!container) return;

  const items = [
    { label: 'Temperature', value: Math.min(Math.abs(values.temperature || 0) * 4, 100), unit: '°C' },
    { label: 'Humidity', value: Math.min(values.humidity || 0, 100), unit: '%' },
    { label: 'Visibility', value: Math.min((values.visibility || 0) * 10, 100), unit: 'km' },
    { label: 'Risk', value: Math.min(values.risk || 0, 100), unit: '%' }
  ];

  container.innerHTML = items.map((item) => `
    <div class="trend-item">
      <div class="trend-header">
        <span>${item.label}</span>
        <strong>${item.value.toFixed(0)}${item.unit}</strong>
      </div>
      <div class="trend-track">
        <div class="trend-fill" style="width: ${item.value}%"></div>
      </div>
    </div>
  `).join('');
}

function renderHistoryChart(riskValue) {
  if (!historyChart) return;

  const safeRisk = Number.isFinite(riskValue) ? riskValue : 0;
  const points = [10, 18, 14, 24, 18, safeRisk, safeRisk + 3];
  const max = 100;
  const width = 300;
  const height = 120;

  const coords = points.map((value, index) => {
    const x = (index / (points.length - 1)) * width;
    const y = height - ((value / max) * 100 + 10);
    return `${x},${y}`;
  }).join(' ');

  const area = `0,${height} ${coords} ${width},${height}`;

  historyChart.innerHTML = `
    <defs>
      <linearGradient id="history-fill" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="rgba(104, 212, 255, 0.7)" />
        <stop offset="100%" stop-color="rgba(104, 212, 255, 0.04)" />
      </linearGradient>
    </defs>
    <polygon points="${area}" fill="url(#history-fill)"></polygon>
    <polyline points="${coords}" fill="none" stroke="#68d4ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"></polyline>
  `;
}

async function fetchWeather(city) {
  try {
    const response = await fetch(`${API_BASE}/weather?city=${encodeURIComponent(city)}`);

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const data = await response.json();
    renderWeather(data);
    renderSkyguard(data);
    renderSafety(data);
    setRouteDefaults(data.weather || {});
    fetchRouteRisk({
      temperature: data.weather?.temperature ?? 23.6,
      humidity: data.weather?.humidity ?? 68,
      pressure: data.weather?.pressure ?? 1011.7,
      rain_probability: 0,
      flood_risk: 0,
      visibility: data.weather?.visibility ?? 9.8
    });
  } catch (error) {
    weatherStatus.textContent = 'Unable to load weather data';
    weatherGrid.innerHTML = '<div class="metric"><label>Error</label><strong>Check backend</strong></div>';
    skyguardScore.textContent = '--';
    safetyScore.textContent = '--';
    console.error(error);
  }
}

async function fetchRouteRisk(values) {
  try {
    const params = new URLSearchParams({
      temperature: values.temperature,
      humidity: values.humidity,
      pressure: values.pressure,
      rain_probability: values.rain_probability,
      flood_risk: values.flood_risk,
      visibility: values.visibility
    });

    const response = await fetch(`${API_BASE}/route-risk?${params.toString()}`);

    if (!response.ok) {
      throw new Error(`Route risk request failed with status ${response.status}`);
    }

    const data = await response.json();
    renderRouteResult(data);
  } catch (error) {
    routeStatus.textContent = 'Error';
    routeDetails.innerHTML = '<div class="info-row"><label>Error</label><span>Route risk request failed.</span></div>';
    console.error(error);
  }
}

cityForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const city = cityInput.value.trim() || 'Bengaluru';
  fetchWeather(city);
});

routeForm.addEventListener('submit', (event) => {
  event.preventDefault();

  const values = {
    temperature: Number(document.getElementById('temperature').value),
    humidity: Number(document.getElementById('humidity').value),
    pressure: Number(document.getElementById('pressure').value),
    rain_probability: Number(document.getElementById('rain_probability').value),
    flood_risk: Number(document.getElementById('flood_risk').value),
    visibility: Number(document.getElementById('visibility').value)
  };

  fetchRouteRisk(values);
});

fetchWeather(cityInput.value || 'Bengaluru');
