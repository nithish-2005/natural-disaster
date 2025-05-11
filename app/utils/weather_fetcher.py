
from flask import Flask, render_template
import requests
import pyttsx3
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

CRITICAL_VALUES = {
    "temperature": 40,
    "humidity": 90,
    "uv_index": 8,
    "wind_speed": 50,
    "pressure": 980,
    "visibility": 1000
}

def voice_alert(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

def send_email_alert(subject, body):
    sender = "your_email@gmail.com"
    password = "your_app_password"
    recipient = "recipient_email@gmail.com"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
            print("Email sent!")
    except Exception as e:
        print("Email failed:", e)

@app.route("/")
def index():
    API_KEY = "your_weather_api_key"
    city = "Chennai"
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=1&aqi=no&alerts=no"

    response = requests.get(url)
    data = response.json()

    current = data["current"]
    forecast = data["forecast"]["forecastday"][0]["hour"][:5]

    temperature = current["temp_c"]
    humidity = current["humidity"]
    wind_speed = current["wind_kph"]
    uv_index = current["uv"]
    pressure = current["pressure_mb"]
    visibility = current["vis_km"]
    rain = current.get("precip_mm", 0)
    location = f"{data['location']['name']}, {data['location']['region']}, {data['location']['country']}"

    hours = [f"{i}h" if i != 0 else "Now" for i in range(5)]
    temperatures = [hour["temp_c"] for hour in forecast]

    alerts = []
    if temperature >= CRITICAL_VALUES["temperature"]:
        alerts.append(f"High Temperature: {temperature}°C")
    if humidity >= CRITICAL_VALUES["humidity"]:
        alerts.append(f"High Humidity: {humidity}%")
    if uv_index >= CRITICAL_VALUES["uv_index"]:
        alerts.append(f"Critical UV Index: {uv_index}")
    if wind_speed >= CRITICAL_VALUES["wind_speed"]:
        alerts.append(f"High Wind Speed: {wind_speed} km/h")
    if pressure <= CRITICAL_VALUES["pressure"]:
        alerts.append(f"Low Pressure: {pressure} hPa")
    if visibility <= CRITICAL_VALUES["visibility"]:
        alerts.append(f"Low Visibility: {visibility} km")

    if alerts:
        alert_msg = "\n".join(alerts)
        voice_alert(alert_msg)
        send_email_alert("🚨 Weather Alert", alert_msg)

    return render_template("index.html",
                           temperature=temperature,
                           humidity=humidity,
                           rain=rain,
                           uv_index=uv_index,
                           wind_speed=wind_speed,
                           pressure=pressure,
                           visibility=visibility,
                           location=location,
                           labels=hours,
                           values=temperatures,
                           alerts=alerts)

if __name__ == "__main__":
    app.run(debug=True)
