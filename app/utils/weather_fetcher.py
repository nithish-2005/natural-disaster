import requests

def fetch_weather_data():
    try:
        api_key = 'YOUR_API_KEY'
        lat = 12.9716
        lon = 77.5946
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'rain': data.get('rain', {}).get('1h', 0),
            'description': data['weather'][0]['description']
        }

    except Exception as e:
        print("Weather fetch failed:", e)
        return {
            'temperature': 0,
            'humidity': 0,
            'wind_speed': 0,
            'rain': 0,
            'description': 'Unable to fetch weather'
        }
