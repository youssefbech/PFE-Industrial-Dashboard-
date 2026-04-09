from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import random
from datetime import datetime
import os
import sys

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("="*50)
print("🚀 Démarrage de l'API...")
print("="*50)

# Essayer de charger les modèles avec plus d'infos
scaler = None
model = None

# Option 1: Chemin absolu Linux
path1 = "/home/mcizdin/PFE/scaler.pkl"
print(f"🔍 Tentative 1: {path1}")
if os.path.exists(path1):
    print(f"✅ Fichier trouvé: {path1}")
    try:
        scaler = joblib.load(path1)
        print(f"✅ Scaler chargé: {type(scaler)}")
    except Exception as e:
        print(f"❌ Erreur chargement scaler: {e}")
else:
    print(f"❌ Fichier non trouvé: {path1}")

path2 = "/home/mcizdin/PFE/svm_model.pkl"
print(f"🔍 Tentative 2: {path2}")
if os.path.exists(path2):
    print(f"✅ Fichier trouvé: {path2}")
    try:
        model = joblib.load(path2)
        print(f"✅ Modèle chargé: {type(model)}")
    except Exception as e:
        print(f"❌ Erreur chargement modèle: {e}")
else:
    print(f"❌ Fichier non trouvé: {path2}")

# Option 2: Chemin relatif (si dans le dossier courant)
if scaler is None:
    path_rel = "scaler.pkl"
    print(f"🔍 Tentative relative: {path_rel}")
    if os.path.exists(path_rel):
        try:
            scaler = joblib.load(path_rel)
            print(f"✅ Scaler chargé (relatif)")
        except Exception as e:
            print(f"❌ Erreur: {e}")

if model is None:
    path_rel = "svm_model.pkl"
    if os.path.exists(path_rel):
        try:
            model = joblib.load(path_rel)
            print(f"✅ Modèle chargé (relatif)")
        except Exception as e:
            print(f"❌ Erreur: {e}")

print(f"\n📊 Statut final:")
print(f"  - Scaler: {'✅ OK' if scaler else '❌ Non chargé'}")
print(f"  - Modèle: {'✅ OK' if model else '❌ Non chargé'}")
print("="*50)

@app.get("/")
def read_root():
    return {"message": "API de prédiction opérationnelle"}

@app.get("/data")
@app.get("/data")
def get_prediction():
    """Simule des données capteurs et retourne une prédiction"""
    
    # Simulation de données (à ajuster selon ton modèle)
    sensor_data = [
        random.uniform(20, 30),    # Température
        random.uniform(40, 60),    # Humidité  
        random.uniform(100, 200),  # Pression
        random.uniform(0, 100),    # CO2
        random.uniform(0, 50),     # TVOC
        random.uniform(0, 1000),   # Particules
        random.uniform(0, 10),     # Bruit
        random.uniform(0, 5)       # Vibrations
    ]
    
    prediction = None
    probability = None
    error_msg = None
    
    if scaler and model:
        try:
            # Convertir en numpy array et normaliser
            X = np.array(sensor_data).reshape(1, -1)
            print(f"Shape des données: {X.shape}")
            
            # Normaliser
            X_scaled = scaler.transform(X)
            
            # Prédire
            pred = model.predict(X_scaled)[0]
            prediction = int(pred)
            
            # Probabilité si disponible
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(X_scaled)[0]
                probability = float(max(proba))
                
        except Exception as e:
            error_msg = str(e)
            print(f"Erreur: {e}")
    
    # Structurer la réponse correctement
    return {
        "timestamp": datetime.now().isoformat(),
        "sensors": {
            "temperature": round(sensor_data[0], 2),
            "humidity": round(sensor_data[1], 2),
            "pressure": round(sensor_data[2], 2),
            "co2": round(sensor_data[3], 2),
            "tvoc": round(sensor_data[4], 2),
            "particles": round(sensor_data[5], 2),
            "noise": round(sensor_data[6], 2),
            "vibration": round(sensor_data[7], 2)
        },
        "prediction": prediction,
        "confidence": probability,
        "status": "normal" if prediction == 0 else "anomalie" if prediction == 1 else "inconnu",
        "debug": {
            "models_loaded": scaler is not None and model is not None,
            "error": error_msg
        }
    }
    """Simule des données capteurs et retourne une prédiction"""
    
    print(f"\n🔄 Nouvelle requête /data à {datetime.now()}")
    
    # Simulation de 8 features
    sensor_data = [
        random.uniform(20, 30),    # Température
        random.uniform(40, 60),    # Humidité
        random.uniform(100, 200),  # Pression
        random.uniform(0, 100),    # CO2
        random.uniform(0, 50),     # TVOC
        random.uniform(0, 1000),   # Particules
        random.uniform(0, 10),     # Bruit
        random.uniform(0, 5)       # Vibrations
    ]
    
    print(f"📊 Données simulées: {[round(x, 2) for x in sensor_data]}")
    
    prediction = None
    probability = None
    error_msg = None
    
    if scaler and model:
        try:
            print("🔄 Normalisation...")
            X_scaled = scaler.transform([sensor_data])
            print(f"✅ Données normalisées: {X_scaled[0][:5]}...")
            
            print("🔄 Prédiction...")
            pred = model.predict(X_scaled)[0]
            prediction = int(pred)
            print(f"✅ Prédiction: {prediction}")
            
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(X_scaled)[0]
                probability = float(max(proba))
                print(f"✅ Probabilité: {probability}")
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ ERREUR: {error_msg}")
            import traceback
            traceback.print_exc()
    else:
        error_msg = "Modèles non chargés"
        print(f"❌ {error_msg}")
    
    response = {
        "timestamp": datetime.now().isoformat(),
        "sensors": {
            "temperature": round(sensor_data[0], 2),
            "humidity": round(sensor_data[1], 2),
            "pressure": round(sensor_data[2], 2),
            "co2": round(sensor_data[3], 2),
            "tvoc": round(sensor_data[4], 2),
            "particles": round(sensor_data[5], 2),
            "noise": round(sensor_data[6], 2),
            "vibration": round(sensor_data[7], 2)
        },
        "prediction": prediction,
        "confidence": probability,
        "status": "normal" if prediction == 0 else "anomalie" if prediction == 1 else "inconnu",
        "debug": {
            "models_loaded": scaler is not None and model is not None,
            "error": error_msg
        }
    }
    
    print(f"📤 Réponse envoyée")
    return response

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "models_loaded": scaler is not None and model is not None,
        "scaler_type": str(type(scaler)) if scaler else None,
        "model_type": str(type(model)) if model else None
    }
