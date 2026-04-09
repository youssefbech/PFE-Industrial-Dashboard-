import paho.mqtt.client as mqtt
import json

# Configuration
TOKEN = "PlEgqU3lgSi87roUYQ9t7oKjrtTeytcfHHUbYiDcfJgk6Ct0SxICHvdOB2jb6TtD" 
BROKER = "mqtt.flespi.io"
TOPIC = "pfe/machine1"

client = mqtt.Client()
client.username_pw_set(TOKEN, "")
client.connect(BROKER, 1883)

# Simulation de l'étape 5 de ton schéma (Anomaly Score)
payload = {
    "vibration": 0.8,
    "temperature": 45.5,
    "anomaly_score": 0.92,
    "status": "ALERTE"
}

client.publish(TOPIC, json.dumps(payload))
print("Données envoyées !")
client.disconnect()