import paho.mqtt.client as mqtt
import json
import joblib
import numpy as np
import time

MODEL_PATH = "svm_model.pkl" 
SCALER_PATH = "scaler.pkl"
# Ajout de ton token Flespi pour la publication vers le Dashboard
FLESPI_TOKEN = "PlEgqU3lgSi87roUYQ9t7oKjrtTeytcfHHUbYiDcfJgk6Ct0SxICHvdOB2jb6TtD"

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
    
    # ⚠️ PUBLICATION SUR FLESPI SUR LE BON TOPIC
    client_pub.publish("motor/M1/data", json.dumps(payload))
    
    status = "✅ NOMINAL" if prediction == 0 else "⚠️ ANOMALIE"
    print(f"[{time.strftime('%H:%M:%S')}] IA -> Flespi | V: {payload['voltage']}V | P: {payload['power']}W | Statut: {status}")

# --- B. CONNEXION LOCALE (Pour écouter le simulateur capteur) ---
client_sub = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client_sub.on_message = on_message
client_sub.connect("localhost", 1883)
client_sub.subscribe("sensor/M1/raw")

print("⚙️ Moteur d'inférence prêt et en attente des données locales...")
client_sub.loop_forever()