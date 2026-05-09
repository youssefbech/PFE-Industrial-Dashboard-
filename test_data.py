import paho.mqtt.client as mqtt
import json, time, random

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)

print("📡 Envoi des données... (Ctrl+C pour arrêter)")

while True:
    payload = {
        "voltage":   round(220 + random.uniform(-5, 5), 2),
        "current":   round(3.5 + random.uniform(-0.5, 0.5), 2),
        "vibration": round(0.02 + random.uniform(0, 0.01), 4),
        "power":     round(750 + random.uniform(-50, 50), 1)
    }
    client.publish("sensors/motor/data", json.dumps(payload))
    print(f"Envoyé : {payload}")
    time.sleep(1)