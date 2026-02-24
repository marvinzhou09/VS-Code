import http.server
import socketserver
import urllib.parse
import requests

PORT = 8000
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your OpenWeatherMap API key
CITIES = [
    ("New York", "US"),
    ("London", "GB"),
    ("Tokyo", "JP"),
    ("Paris", "FR"),
    ("Sydney", "AU"),
    ("Mumbai", "IN"),
    ("Beijing", "CN"),
    ("Moscow", "RU"),
    ("Rio de Janeiro", "BR"),
    ("Cape Town", "ZA"),
]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 0; }
        .container { max-width: 400px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 32px; }
        h1 { text-align: center; color: #333; }
        select, button { width: 100%; padding: 10px; margin: 12px 0; border-radius: 6px; border: 1px solid #ccc; font-size: 16px; }
        .weather { margin-top: 24px; text-align: center; }
        .temp { font-size: 32px; color: #0077b6; }
        .desc { font-size: 18px; color: #555; }
        .unit-toggle { margin-top: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Weather App</h1>
        <form method="get">
            <label for="city">Select City:</label>
            <select name="city" id="city">
                {city_options}
            </select>
            <div class="unit-toggle">
                <label><input type="radio" name="unit" value="metric" {metric_checked}> Celsius (°C)</label>
                <label><input type="radio" name="unit" value="imperial" {imperial_checked}> Fahrenheit (°F)</label>
            </div>
            <button type="submit">Get Weather</button>
        </form>
        {weather_html}
    </div>
</body>
</html>
'''

class WeatherHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        city = params.get('city', [CITIES[0][0]])[0]
        unit = params.get('unit', ['metric'])[0]
        weather_html = ""
        if 'city' in params:
            weather_html = self.get_weather_html(city, unit)
        city_options = "".join([
            f'<option value="{c[0]}"' + (" selected" if c[0] == city else "") + f'>{c[0]}</option>'
            for c in CITIES
        ])
        metric_checked = "checked" if unit == "metric" else ""
        imperial_checked = "checked" if unit == "imperial" else ""
        html = HTML_TEMPLATE.format(
            city_options=city_options,
            weather_html=weather_html,
            metric_checked=metric_checked,
            imperial_checked=imperial_checked
        )
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def get_weather_html(self, city, unit):
        country = next((c[1] for c in CITIES if c[0] == city), "US")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units={unit}"
        try:
            resp = requests.get(url)
            data = resp.json()
            if resp.status_code != 200:
                return f'<div class="weather"><span class="desc">Error: {data.get("message", "Unknown error")}</span></div>'
            temp = data['main']['temp']
            desc = data['weather'][0]['description'].title()
            icon = data['weather'][0]['icon']
            icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
            unit_symbol = "°C" if unit == "metric" else "°F"
            return f'''<div class="weather">
                <img src="{icon_url}" alt="Weather icon" style="width:80px;height:80px;">
                <div class="temp">{temp} {unit_symbol}</div>
                <div class="desc">{desc}</div>
            </div>'''
        except Exception as e:
            return f'<div class="weather"><span class="desc">Error: {str(e)}</span></div>'

if __name__ == "__main__":
    print(f"Starting server at http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), WeatherHandler) as httpd:
        httpd.serve_forever()
