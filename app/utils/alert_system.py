from gtts import gTTS
from playsound import playsound
import smtplib
from email.mime.text import MIMEText
from app.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

def send_voice_alert(message):
    tts = gTTS(text=message, lang='en')
    tts.save("alert.mp3")
    playsound("alert.mp3")

def send_email_alert(weather, risk):
    body = f"""ALERT: {risk} Flood Risk Detected!
Current Weather:
Temperature: {weather['temperature']}°C
Humidity: {weather['humidity']}%
Wind Speed: {weather['wind_speed']} km/h
Rain (last 1h): {weather['rain']} mm
Description: {weather['description']}
"""
    msg = MIMEText(body)
    msg['Subject'] = "Weather Alert"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

def send_alerts(weather, risk):
    alert_msg = f"Alert! {risk} flood risk detected. Stay safe!"
    send_voice_alert(alert_msg)
    send_email_alert(weather, risk)
