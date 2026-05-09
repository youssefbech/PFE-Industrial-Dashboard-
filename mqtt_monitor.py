#!/usr/bin/env python3
"""
Moniteur MQTT - Affiche tout ce qui transite sur les topics importants
"""

import paho.mqtt.client as mqtt
import json
from datetime import datetime

BROKER = "localhost"
PORT = 1883

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connecté au Broker MQTT")
        # Écouter tous les topics
        client.subscribe("sensor/M1/raw")
        client.subscribe("motor/M1/data")
        client.subscribe("sensor/+/raw")
        client.subscribe("motor/+/data")
    else:
        print(f"❌ Connexion échouée, code : {rc}")

def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    
    try:
        payload = json.loads(msg.payload.decode())
        payload_str = json.dumps(payload, indent=2)
    except:
        payload_str = msg.payload.decode()
    
    print(f"\n[{timestamp}] Topic: {msg.topic}")
    print(f"Payload:\n{payload_str}")
    print("─" * 60)

# Initialiser le client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print(f"🔌 Connexion au broker MQTT {BROKER}:{PORT} ...")
client.connect(BROKER, PORT, 60)

print("📡 Écoute des topics :")
print("  • sensor/M1/raw (ESP32)")
print("  • motor/M1/data (test_val_mqtt.py)")
print("\nEn attente de messages...\n")

client.loop_forever()
