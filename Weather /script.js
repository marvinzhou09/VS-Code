const citySelect = document.getElementById("citySelect");
const unitSelect = document.getElementById("unitSelect");
const loadWeatherBtn = document.getElementById("loadWeatherBtn");
const weatherPanel = document.getElementById("weatherPanel");

const majorCities = [
  { name: "New York, USA", latitude: 40.7128, longitude: -74.006 },
  { name: "Los Angeles, USA", latitude: 34.0522, longitude: -118.2437 },
  { name: "London, UK", latitude: 51.5072, longitude: -0.1276 },
  { name: "Paris, France", latitude: 48.8566, longitude: 2.3522 },
  { name: "Tokyo, Japan", latitude: 35.6762, longitude: 139.6503 },
  { name: "Dubai, UAE", latitude: 25.2048, longitude: 55.2708 },
  { name: "Sydney, Australia", latitude: -33.8688, longitude: 151.2093 },
  { name: "Singapore", latitude: 1.3521, longitude: 103.8198 },
  { name: "Cairo, Egypt", latitude: 30.0444, longitude: 31.2357 },
  { name: "Cape Town, South Africa", latitude: -33.9249, longitude: 18.4241 },
  { name: "Rio de Janeiro, Brazil", latitude: -22.9068, longitude: -43.1729 },
  { name: "Toronto, Canada", latitude: 43.6532, longitude: -79.3832 },
  { name: "Mumbai, India", latitude: 19.076, longitude: 72.8777 },
  { name: "Seoul, South Korea", latitude: 37.5665, longitude: 126.978 },
  { name: "Mexico City, Mexico", latitude: 19.4326, longitude: -99.1332 },
  { name: "Beijing, China", latitude: 39.9042, longitude: 116.4074 },
  { name: "Shenzhen, China", latitude: 22.5431, longitude: 114.0579 }
];

const weatherCodeMap = {
  0: "Clear sky",
  1: "Mostly clear",
  2: "Partly cloudy",
  3: "Overcast",
  45: "Fog",
  48: "Depositing rime fog",
  51: "Light drizzle",
  53: "Moderate drizzle",
  55: "Dense drizzle",
  56: "Freezing drizzle",
  57: "Heavy freezing drizzle",
  61: "Slight rain",
  63: "Moderate rain",
  65: "Heavy rain",
  66: "Light freezing rain",
  67: "Heavy freezing rain",
  71: "Slight snow",
  73: "Moderate snow",
  75: "Heavy snow",
  77: "Snow grains",
  80: "Slight rain showers",
  81: "Moderate rain showers",
  82: "Violent rain showers",
  85: "Slight snow showers",
  86: "Heavy snow showers",
  95: "Thunderstorm",
  96: "Thunderstorm with slight hail",
  99: "Thunderstorm with heavy hail"
};

function populateCities() {
  majorCities.forEach((city, index) => {
    const option = document.createElement("option");
    option.value = String(index);
    option.textContent = city.name;
    citySelect.append(option);
  });
}

function renderLoading() {
  weatherPanel.innerHTML = '<p class="hint">Loading weather data...</p>';
}

function renderError(message) {
  weatherPanel.innerHTML = `<p class="error">${message}</p>`;
}

function renderWeather(cityName, weather, unitSymbol) {
  const description = weatherCodeMap[weather.weather_code] || "Unknown conditions";
  const time = new Date(weather.time).toLocaleString();

  weatherPanel.innerHTML = `
    <h2 class="city">${cityName}</h2>
    <p class="temp">${weather.temperature_2m}${unitSymbol}</p>
    <p class="details">${description}</p>
    <p class="details">Wind: ${weather.wind_speed_10m} km/h</p>
    <p class="details">Updated: ${time}</p>
  `;
}

async function loadWeather() {
  const selectedCityIndex = Number(citySelect.value);
  const unit = unitSelect.value;
  const unitSymbol = unit === "fahrenheit" ? "°F" : "°C";
  const city = majorCities[selectedCityIndex];

  if (!city) {
    renderError("Please select a city.");
    return;
  }

  renderLoading();

  const url = new URL("https://api.open-meteo.com/v1/forecast");
  url.searchParams.set("latitude", city.latitude);
  url.searchParams.set("longitude", city.longitude);
  url.searchParams.set("current", "temperature_2m,weather_code,wind_speed_10m");
  url.searchParams.set("temperature_unit", unit);
  url.searchParams.set("timezone", "auto");

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("Weather service unavailable.");
    }

    const data = await response.json();
    if (!data.current) {
      throw new Error("No weather data returned for this city.");
    }

    renderWeather(city.name, data.current, unitSymbol);
  } catch (error) {
    renderError(error.message || "Failed to load weather data.");
  }
}

populateCities();
loadWeatherBtn.addEventListener("click", loadWeather);
