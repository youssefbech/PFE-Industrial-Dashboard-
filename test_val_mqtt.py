import paho.mqtt.client as mqtt
import json
import time
import joblib
import numpy as np
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
BROKER         = "192.168.137.39"    # IP de la Raspberry Pi (interface wlan0)
PORT           = 1883
TOPIC_RAW      = "sensor/M1/raw"     # topic reçu depuis l'ESP32
TOPIC_PROCESSED = "motor/M1/data"    # ✅ topic que le dashboard écoute (motor/+/data)

# Chargement du modèle SVM et du scaler (décommenter quand tu as les fichiers)
# svm_model = joblib.load("svm_model.pkl")
# scaler    = joblib.load("scaler.pkl")

# ─────────────────────────────────────────────
# ÉTAT GLOBAL
# ─────────────────────────────────────────────
last_voltage_adapted = 24.0   # Pour calculer Delta_V

# ─────────────────────────────────────────────
# CALLBACKS MQTT
# ─────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connecté au Broker MQTT (localhost)")
        client.subscribe(TOPIC_RAW)
        print(f"📡 Abonné au topic : {TOPIC_RAW}")
    else:
        print(f"❌ Connexion échouée, code : {rc}")


def on_message(client, userdata, msg):
    """
    BUG CORRIGÉ : toute la logique (calcul + publish) est DANS on_message.
    Avant : le publish était APRÈS loop_forever() → jamais exécuté.
    """
    global last_voltage_adapted

    try:
        # ── 1. Lire le JSON de l'ESP32 (déjà en vraies valeurs) ──────────
        data      = json.loads(msg.payload.decode())
        voltage_v = data.get("tension", 0)      # Déjà en volts (ex: 24.5)
        current_a = data.get("courant", 0)      # Déjà en ampères (ex: 2.1)


        # ── 2. Les valeurs sont déjà en vraies unités, pas de conversion ──
        # L'ESP32 a déjà fait la conversion avec ses diviseurs
        if current_a < 0.20:
            current_a = 0.0

        # ── 3. Calculer les features manquantes ───────────────────────────
        power_w      = voltage_v * current_a
        delta_v      = voltage_v - last_voltage_adapted
        temperature_c = 36.0   # fixe (pas de capteur de température branché)

        # Mise à jour pour la prochaine itération
        last_voltage_adapted = voltage_v

        # ── 4. Détection d'anomalie : courant nul = fault_label 1 ─────────
        if current_a == 0.0:
            fault_label = 1
            anomaly_score = 1
        else:
            fault_label = 0
            anomaly_score = 0

        # (Si tu veux utiliser le modèle SVM plus tard, insère la logique ici)
        # vecteur = np.array([[current_a, voltage_v, temperature_c, power_w, delta_v]])
        # vecteur_scaled = scaler.transform(vecteur)
        # prediction     = svm_model.predict(vecteur_scaled)
        # fault_label    = int(prediction[0])
        # anomaly_score  = fault_label

        # ── 5. Construire le JSON complet avec les clés attendues par le dashboard
        #       BUG CORRIGÉ : les clés correspondent exactement à ce que
        #       dashboard_pfe.py lit (voltage, current, power, temp, anomaly_score)
        timestamp = datetime.now().strftime("%H:%M:%S")
        data_processed = {
            "timestamp"    : timestamp,
            "voltage"      : round(voltage_v, 2),    # ✅ clé correcte
            "current"      : round(current_a, 2),    # ✅ clé correcte
            "power"        : round(power_w, 2),      # ✅ clé correcte
            "temp"         : round(temperature_c, 1),# ✅ clé correcte
            "delta_v"      : round(delta_v, 3),
            "fault_label"  : fault_label,
            "anomaly_score": anomaly_score,
        }

        # ── 6. Publier sur le topic que le dashboard écoute ───────────────
        #       BUG CORRIGÉ : topic = "motor/M1/data" (au lieu de "sensor/M1/processed")
        client.publish(TOPIC_PROCESSED, json.dumps(data_processed))

        # ── 7. Log console ────────────────────────────────────────────────
        status = "⚠️ ANOMALIE" if fault_label != 0 else "✅ NORMAL"
        print(
            f"[{timestamp}] "
            f"V: {voltage_v:>6.2f}V | I: {current_a:>5.2f}A | "
            f"P: {power_w:>6.2f}W | ΔV: {delta_v:>6.3f} | "
            f"T: {temperature_c}°C | {status}"
        )

    except Exception as e:
        print(f"❌ Erreur dans on_message : {e}")


# ─────────────────────────────────────────────
# LANCEMENT DU CLIENT MQTT
# ─────────────────────────────────────────────
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print(f"🔌 Connexion à {BROKER}:{PORT} ...")
client.connect(BROKER, PORT, 60)

# loop_forever() est EN DERNIER → il bloque et appelle on_message à chaque message
# BUG CORRIGÉ : le publish est DANS on_message, pas après loop_forever()
client.loop_forever()