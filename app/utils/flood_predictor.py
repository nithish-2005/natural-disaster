def predict_flood_risk(weather_data):
    try:
        rain = float(weather_data.get('rain', 0)) if weather_data.get('rain', 0) != 'N/A' else 0
        humidity = float(weather_data.get('humidity', 0)) if weather_data.get('humidity', 0) != 'N/A' else 0
    except Exception as e:
        print("Data format error:", e)
        return "Unknown"

    if rain > 80 and humidity > 85:
        return "High"
    elif rain > 50:
        return "Moderate"
    else:
        return "Low"
