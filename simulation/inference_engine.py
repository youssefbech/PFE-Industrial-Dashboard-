import paho.mqtt.client as mqtt
import json
import joblib
import numpy as np
import time
import os
import requests
from datetime import datetime

# Configuration Telegram
TOKEN = "8745092490:AAGdGElqCe6nqAtCJ_roXaBchUxknBsVLXU"
CHAT_ID = "8179717946"

def send_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message
        }
        requests.post(url, data=data)
    except Exception as e:
        print(f"❌ Erreur Telegram: {e}")

MODEL_PATH = "/home/pi/PFE/simulation/svm_model.pkl"
SCALER_PATH = "/home/pi/PFE/simulation/scaler.pkl"
DATA_FILE = "/tmp/motor_data.json"
# Ajout de ton token Flespi pour la publication vers le Dashboard
FLESPI_TOKEN = "PlEgqU3lgSi87roUYQ9t7oKjrtTeytcfHHUbYiDcfJgk6Ct0SxICHvdOB2jb6TtD"

# Fonction pour sauvegarder les données dans un fichier
def save_motor_data(motor_id, payload):
    data = {}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
        except:
            pass
    
    if motor_id not in data:
        data[motor_id] = []
    
    payload['Time'] = datetime.now().strftime("%H:%M:%S")
    data[motor_id].append(payload)
    
    # Garder seulement les 60 dernières entrées
    if len(data[motor_id]) > 60:
        data[motor_id] = data[motor_id][-60:]
    
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# 1. Chargement des modèles
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("✅ Modèle SVM et Scaler chargés avec succès.")
except Exception as e:
    print(f"❌ Erreur de chargement : {e}")
    exit()

# --- A. CONNEXION CLOUD (Pour envoyer au Dashboard) ---
# Utilisation de la VERSION2 pour éviter les warnings, comme dans ton Dashboard
client_pub = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client_pub.username_pw_set(FLESPI_TOKEN, "")
client_pub.connect("mqtt.flespi.io", 1883)

# --- A2. CONNEXION LOCALE (Pour le Dashboard local) ---
client_local = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client_local.connect("localhost", 1883)

# 2. Traitement à chaque réception du simulateur local
def on_message(client, userdata, msg):
    raw = json.loads(msg.payload.decode())
    
    # Extraction des données BRUTES
    features = np.array([[
        raw.get('Timestamp', 0), 
        raw['Current_A'], 
        raw['Voltage_V'], 
        raw['Temperature_C'], 
        raw['Power_W'], 
        raw.get('Delta_V', 0)
    ]])
    
    # Standardisation UNIQUEMENT pour l'IA
    scaled_features = scaler.transform(features)
    
    # Inférence (Prédiction)
    prediction = model.predict(scaled_features)[0]
    
    # Envoi au Dashboard (On renvoie les données brutes formatées + le score)
    payload = {
        "current": float(raw['Current_A']),
        "voltage": float(raw['Voltage_V']),
        "temp": float(raw['Temperature_C']),
        "power": float(raw['Power_W']),
        "anomaly_score": int(prediction)
    }
    
    # PUBLICATION SUR LE BROKER LOCAL SUR LE TOPIC sensors/motor/test
    client_local.publish("sensors/motor/test", json.dumps(payload))
    
    # Sauvegarde dans un fichier pour le Dashboard Streamlit
    save_motor_data("M1", payload)
    
    status = "✅ NOMINAL" if prediction == 0 else "⚠️ ANOMALIE"
    print(f"[{time.strftime('%H:%M:%S')}] IA -> Flespi | V: {payload['voltage']}V | P: {payload['power']}W | Statut: {status}")
    
    # Envoi alerte Telegram si anomalie détectée
    if prediction != 0:
        alert_msg = f"🚨 ANOMALIE DÉTECTÉE !\nMachine: M1\nTension: {payload['voltage']:.2f}V\nCourant: {payload['current']:.2f}A\nPuissance: {payload['power']:.2f}W\nScore: {prediction}"
        send_alert(alert_msg)

# --- B. CONNEXION LOCALE (Pour écouter le simulateur capteur) ---
client_sub = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client_sub.on_message = on_message
client_sub.connect("localhost", 1883)
client_sub.subscribe("sensor/M1/raw")

print("⚙️ Moteur d'inférence prêt et en attente des données locales...")
client_sub.loop_forever()
