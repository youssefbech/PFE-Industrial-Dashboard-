#!/usr/bin/env python3
"""
Script de test pour le système PFE complet:
- Simulateur → MQTT local (sensor/M1/raw)
- Inference Engine → MQTT local + Flespi (motor/M1/data)
- Dashboard → MQTT local (motor/+/data)
"""

import subprocess
import time
import sys
import os

# Couleurs pour le terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_status(msg, status="info"):
    colors = {"ok": GREEN, "error": RED, "warn": YELLOW, "info": BLUE}
    print(f"{colors.get(status, '')}[{status.upper()}]{RESET} {msg}")

def main():
    print(f"""
{BLUE}========================================
   TEST SYSTÈME PFE - SIMULATION + IA
========================================{RESET}
    """)
    
    # Vérifier que les fichiers nécessaires existent
    print_status("Vérification des fichiers...", "info")
    
    required_files = {
        "simulateur.py": "/home/pi/PFE/simulation/simulateur.py",
        "inference_engine.py": "/home/pi/PFE/simulation/inference_engine.py",
        "dashboard.py": "/home/pi/PFE/simulation/dashboard.py",
        "dataset": "/home/pi/PFE/simulation/bldc_predictive_maintenance_dataset (1) (1) (1).csv",
        "svm_model.pkl": "/home/pi/PFE/svm_model.pkl",
        "scaler.pkl": "/home/pi/PFE/scaler.pkl",
    }
    
    missing = []
    for name, path in required_files.items():
        if os.path.exists(path):
            print_status(f"✓ {name} trouvé", "ok")
        else:
            print_status(f"✗ {name} manquant: {path}", "error")
            missing.append(name)
    
    if missing:
        print_status(f"Fichiers manquants: {', '.join(missing)}", "error")
        return 1
    
    print(f"""
{BLUE}========================================
   ARCHITECTURE DU SYSTÈME
========================================{RESET}

{YELLOW}1. SIMULATEUR{RESET}
   └─> Envoie données brutes vers MQTT local
   └─> Topic: sensor/M1/raw

{YELLOW}2. INFERENCE ENGINE{RESET}
   └─> Écoute: sensor/M1/raw (MQTT local)
   └─> Applique: SVM + Scaler
   └─> Publie: motor/M1/data (MQTT local + Flespi)

{YELLOW}3. DASHBOARD{RESET}
   └─> Écoute: motor/+/data (MQTT local)
   └─> Affiche: Métriques temps réel + Anomalies

{GREEN}Pour tester, lancez dans 3 terminaux séparés:{RESET}

Terminal 1 (Inference Engine):
  cd /home/pi/PFE/simulation
  python inference_engine.py

Terminal 2 (Simulateur):
  cd /home/pi/PFE/simulation
  python simulateur.py

Terminal 3 (Dashboard):
  cd /home/pi/PFE/simulation
  streamlit run dashboard.py

{RESET}""")
    
    # Test de connexion MQTT
    print_status("Test de connexion MQTT...", "info")
    try:
        import paho.mqtt.client as mqtt
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.connect("localhost", 1883, timeout=5)
        print_status("✓ MQTT local connecté", "ok")
        client.disconnect()
    except Exception as e:
        print_status(f"✗ MQTT local: {e}", "error")
        print_status("Démarrez le broker MQTT: mosquitto", "warn")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())