import json
import numpy as np
# import joblib  # Pour charger ton modèle et ton scaler

# Variable globale pour calculer le Delta_V
tension_precedente_adaptee = 24.0 

def adapter_donnees_pour_svm(payload_mqtt_brut):
    global tension_precedente_adaptee
    
    # 1. Extraction des données de l'ESP32
    data = json.loads(payload_mqtt_brut)
    tension_raw = data["tension"]
    courant_raw = data["courant"]
    
    # 2. Mise à l'échelle (Mapping vers le domaine d'entraînement 24V/2A)
    # Ces coefficients transforment tes lectures 7V en équivalent 24V
    coef_tension = 24.0 / 6.94
    coef_courant = 2.15 / 0.23
    
    voltage_v = tension_raw * coef_tension
    # Éviter d'amplifier le bruit si le courant est à 0
    current_a = courant_raw * coef_courant if courant_raw > 0 else 0.0
    
    # 3. Création des variables (Features) manquantes
    power_w = voltage_v * current_a
    delta_v = voltage_v - tension_precedente_adaptee
    temperature_c = 36.0  # Valeur nominale fixe simulée
    
    # Mise à jour pour la prochaine itération
    tension_precedente_adaptee = voltage_v
    
    # 4. Construction du vecteur dans l'ordre EXACT du CSV
    # [Current_A, Voltage_V, Temperature_C, Power_W, Delta_V]
    vecteur_features = np.array([[current_a, voltage_v, temperature_c, power_w, delta_v]])
    
    return vecteur_features, voltage_v, current_a, power_w, delta_v, temperature_c

# --- Exemple d'utilisation à l'arrivée d'un message MQTT ---
message_mqtt = '{"tension": 6.72, "courant": 0.232}'

# 1. Extraction des données brutes pour l'affichage
data = json.loads(message_mqtt)
tension_raw = data["tension"]
courant_raw = data["courant"]

# 2. On adapte les données
X_new, voltage_v, current_a, power_w, delta_v, temperature_c = adapter_donnees_pour_svm(message_mqtt)

# 2. Normalisation (TRÈS IMPORTANT)
# Tu dois utiliser l'objet StandardScaler ou MinMaxScaler que tu as 
# ajusté (fit) pendant l'entraînement de ton modèle SVM.
# X_new_scaled = mon_scaler.transform(X_new)

# 3. Prédiction
# prediction = mon_modele_svm.predict(X_new_scaled)
# print("Prédiction de panne :", prediction[0])
# À l'intérieur de ton callback MQTT (on_message)
print("-" * 30)
print(f"📥 RECU (ESP32)  : Tension: {tension_raw}V, Courant: {courant_raw}A")

# Après avoir appliqué les coefficients de ma réponse précédente
print(f"🔄 ADAPTÉ (SVM) : Voltage: {voltage_v:.2f}V, Current: {current_a:.2f}A")
print(f"📊 FEATURES     : Power: {power_w:.2f}W, Delta_V: {delta_v:.2f}, Temp: {temperature_c}°C")
print("-" * 30)
import paho.mqtt.client as mqtt
import json
import time

# Variables pour le calcul du Delta_V
last_voltage_adapted = 24.0

def on_connect(client, userdata, flags, rc):
    print("✅ Connecté au Broker MQTT")
    client.subscribe("sensor/M1/raw")

def on_message(client, userdata, msg):
    global last_voltage_adapted
    try:
        # 1. Décoder le JSON reçu de l'ESP32
        data = json.loads(msg.payload.decode())
        tension_raw = data.get("tension", 0)
        courant_raw = data.get("courant", 0)

        # 2. Transformation (Adaptation au modèle SVM 24V/2A)
        # Coéfficients basés sur tes captures d'écran
        voltage_v = tension_raw * (24.0 / 6.94)
        current_a = courant_raw * (2.15 / 0.23) if courant_raw > 0 else 0.0
        
        # 3. Calcul des Features manquantes
        power_w = voltage_v * current_a
        delta_v = voltage_v - last_voltage_adapted
        temperature_c = 36.0  # Valeur fixe pour stabiliser le SVM
        
        # Mise à jour de la tension pour le prochain calcul de Delta_V
        last_voltage_adapted = voltage_v

        # 4. Affichage TOUTES LES VALEURS (Une ligne par seconde)
        # Le formatage .2f permet de limiter à 2 décimales pour la lisibilité
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] V_adapt: {voltage_v:>5.2f}V | I_adapt: {current_a:>5.2f}A | P: {power_w:>5.2f}W | ΔV: {delta_v:>6.2f} | Temp: {temperature_c}°C")

    except Exception as e:
        print(f"❌ Erreur : {e}")

# Configuration du client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Lancer la boucle infinie pour voir les valeurs défiler
client.loop_forever()
# Dans ton script test_val_mqtt.py, à la fin de la fonction on_message :

# 1. On crée un nouveau dictionnaire avec les valeurs adaptées
data_traitee = {
    "tension": round(voltage_v, 2),
    "courant": round(current_a, 2),
    "puissance": round(power_w, 2),
    "temperature": temperature_c
}

# 2. On envoie ce JSON sur un nouveau topic
client.publish("sensor/M1/processed", json.dumps(data_traitee))