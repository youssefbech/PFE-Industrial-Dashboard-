# Exemple de code pour charger et utiliser le modèle sauvegardé
import joblib
import pandas as pd
import numpy as np

# Charger le modèle et le scaler
svm_model = joblib.load('svm_model.pkl')
scaler = joblib.load('scaler.pkl')

# Pour faire des prédictions sur de nouvelles données
def predict_new_data(new_data):
    """
    new_data: DataFrame avec les mêmes colonnes que les données d'entraînement
    """
    # Normaliser
    new_data_scaled = scaler.transform(new_data)
    # Prédire
    predictions = svm_model.predict(new_data_scaled)
    probas = svm_model.predict_proba(new_data_scaled)
    return predictions, probas

# Exemple d'utilisation
# predictions, probas = predict_new_data(nouveaux_echantillons)