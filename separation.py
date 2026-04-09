import pandas as pd
import numpy as np

# Charger les données
df = pd.read_csv('dataset_standardized.csv')

# 1. S'assurer que les données sont triées par le temps (ordre chronologique)
#    Les timestamps sont probablement décroissants (du plus récent au plus ancien)
#    Nous les trions par ordre croissant (ancien -> récent)
df = df.sort_values(by='Timestamp', ascending=True).reset_index(drop=True)

print("Aperçu des données triées (ancien en haut):")
print(df.head())
print("\nAperçu des données triées (récent en bas):")
print(df.tail())

# 2. Calculer l'index de séparation
train_size = 0.8
split_index = int(len(df) * train_size)

# 3. Séparer les données
train_data = df.iloc[:split_index]   # Les 80% les plus anciens
validation_data = df.iloc[split_index:]    # Les 20% les plus récents

# Afficher la taille des ensembles résultants
print(f"\nTaille totale du dataset : {len(df)}")
print(f"Taille de l'ensemble d'entraînement (80% anciens) : {len(train_data)}")
print(f"Taille de l'ensemble de validation (20% récents) : {len(validation_data)}")

# 4. Exporter vers des fichiers CSV
train_data.to_csv('train_data.csv', index=False)
validation_data.to_csv('validation_data.csv', index=False)

print("\n✅ Fichiers exportés avec succès :")
print("   - train_data.csv")
print("   - validation_data.csv")

# 5. (Optionnel) Vérification rapide des premières lignes des fichiers exportés
print("\nPremières lignes du fichier d'entraînement :")
print(pd.read_csv('train_data.csv').head())
print("\nPremières lignes du fichier de validation :")
print(pd.read_csv('validation_data.csv').head())