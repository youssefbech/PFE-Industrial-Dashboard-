import paho.mqtt.client as mqtt
import json
import time

# --- CONFIGURATION ---
TOKEN = "PlEgqU3lgSi87roUYQ9t7oKjrtTeytcfHHUbYiDcfJgk6Ct0SxICHvdOB2jb6TtD"  # <--- Colle ton token ici
BROKER = "mqtt.flespi.io"
PORT = 1883
TOPIC = "pfe/machine1/telemetry"

# --- CONNEXION ---
client = mqtt.Client()
client.username_pw_set(TOKEN, "") # Le mot de passe reste vide sur Flespi

print("Connexion au broker Flespi...")
client.connect(BROKER, PORT)

# --- ENVOI DE DONNÉES ---
# On simule un message de ton IA
data = {
    "vibration": 0.45,
    "temperature": 38.2,
    "anomaly_score": 0.05,
    "status": "NORMAL"
}

print(f"Envoi du message sur le topic : {TOPIC}")
client.publish(TOPIC, json.dumps(data))

print("Message envoyé ! Vérifie maintenant sur Flespi.")
client.disconnect()