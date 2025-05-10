from flask import render_template
from app import app
from app.utils.weather_fetcher import fetch_weather_data
from app.utils.flood_predictor import predict_flood_risk
from app.utils.alert_system import send_alerts

@app.route('/')
def index():
    weather_data = fetch_weather_data()
    flood_risk = predict_flood_risk(weather_data)
    if flood_risk == 'High':
        send_alerts(weather_data, flood_risk)
    return render_template('index.html', weather=weather_data, risk=flood_risk)
