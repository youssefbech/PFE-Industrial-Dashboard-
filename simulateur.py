import pandas as pd
import paho.mqtt.client as mqtt
import time
import json

# ⚠️ TRÈS IMPORTANT : Ce fichier DOIT contenir tes valeurs physiques brutes (ex: Tension=220V), 
# et surtout PAS les valeurs standardisées.
csv_file = 'bldc_predictive_maintenance_dataset (1) (1) (1).csv' 

try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"❌ Erreur : Le fichier {csv_file} est introuvable. Mets le bon nom de fichier brut.")
    exit()

client = mqtt.Client()
client.connect("localhost", 1883)

print("🚀 Simulateur de capteurs démarré (Vitesse: 0.1s)...")

for index, row in df.iterrows():
    # On récupère les valeurs BRUTES du CSV
    data = {
        "Timestamp": row.get('Timestamp', 0), 
        "Current_A": row['Current_A'],
        "Voltage_V": row['Voltage_V'],
        "Temperature_C": row['Temperature_C'],
        "Power_W": row['Power_W'],
        "Delta_V": row.get('Delta_V', 0)
    }
    
    # Envoi au moteur d'IA
    client.publish("sensor/M1/raw", json.dumps(data))
    print(f"📡 Envoi Brut -> V: {data['Voltage_V']}V | A: {data['Current_A']}A")
    
    time.sleep(0.1) # Vitesse modifiée à 0.1 seconde comme demandé