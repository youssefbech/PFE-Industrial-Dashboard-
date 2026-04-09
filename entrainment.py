import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# ============================================
# 1. CHARGEMENT DES DONNÉES
# ============================================
print("📂 Chargement des données...")
train_data = pd.read_csv('train_data.csv')
validation_data = pd.read_csv('validation_data.csv')

# Séparer features (X) et target (y)
X_train = train_data.drop('Fault_Label', axis=1)
y_train = train_data['Fault_Label']
X_val = validation_data.drop('Fault_Label', axis=1)
y_val = validation_data['Fault_Label']

print(f"✅ Données chargées:")
print(f"   - Train: {X_train.shape[0]} échantillons, {X_train.shape[1]} features")
print(f"   - Validation: {X_val.shape[0]} échantillons, {X_val.shape[1]} features")
print(f"\n   Distribution des classes:")
print(f"   Train:\n{y_train.value_counts().sort_index()}")
print(f"   Validation:\n{y_val.value_counts().sort_index()}")

# ============================================
# 2. NORMALISATION DES DONNÉES (TRÈS IMPORTANT POUR SVM)
# ============================================
print("\n⚙️ Normalisation des données...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
print("✅ Normalisation terminée")

# ============================================
# 3. ENTRAÎNEMENT DU SVM
# ============================================
print("\n🎯 Entraînement du SVM...")

# Création du modèle avec de bons paramètres par défaut
svm_model = SVC(
    kernel='rbf',           # Noyau RBF (bon pour la plupart des cas)
    C=10,                   # Paramètre de régularisation (10 est un bon compromis)
    gamma='scale',          # Gamma automatique
    class_weight='balanced', # Gère automatiquement le déséquilibre des classes
    random_state=42,
    probability=True        # Pour avoir les probabilités si besoin
)

# Entraînement
svm_model.fit(X_train_scaled, y_train)
print("✅ Entraînement terminé !")

# ============================================
# 4. ÉVALUATION DU MODÈLE
# ============================================
print("\n📊 Évaluation du modèle...")

# Prédictions
y_pred = svm_model.predict(X_val_scaled)

# Calcul de la précision
accuracy = accuracy_score(y_val, y_pred)
print(f"\n🎯 Précision sur l'ensemble de validation: {accuracy:.4f}")

# Rapport de classification détaillé
print("\n📋 Rapport de classification:")
print(classification_report(y_val, y_pred))

# ============================================
# 5. VISUALISATION DE LA MATRICE DE CONFUSION
# ============================================
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_val, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=sorted(y_val.unique()), 
            yticklabels=sorted(y_val.unique()))
plt.title(f'Matrice de Confusion - SVM\nPrécision: {accuracy:.3f}')
plt.xlabel('Prédictions')
plt.ylabel('Vérités')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150)
plt.show()
print("✅ Matrice de confusion sauvegardée: confusion_matrix.png")

# ============================================
# 6. ANALYSE DES ERREURS (OPTIONNEL)
# ============================================
# Identifier les indices où le modèle se trompe
errors = (y_val != y_pred)
print(f"\n❌ Nombre d'erreurs de classification: {errors.sum()} / {len(y_val)}")

if errors.sum() > 0:
    print("\nExemples d'erreurs (5 premiers):")
    error_indices = np.where(errors)[0][:5]
    for idx in error_indices:
        print(f"   Index {idx}: Vrai={y_val.iloc[idx]}, Prédit={y_pred[idx]}")

# ============================================
# 7. SAUVEGARDE DU MODÈLE
# ============================================
print("\n💾 Sauvegarde du modèle...")
joblib.dump(svm_model, 'svm_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("✅ Modèle sauvegardé: svm_model.pkl")
print("✅ Scaler sauvegardé: scaler.pkl")

# ============================================
# 8. TEST SUR QUELQUES ÉCHANTILLONS (OPTIONNEL)
# ============================================
print("\n🔍 Test sur 5 échantillons de validation:")
sample_indices = np.random.choice(len(X_val), 5, replace=False)
for i, idx in enumerate(sample_indices):
    vrai = y_val.iloc[idx]
    pred = svm_model.predict(X_val_scaled[idx].reshape(1, -1))[0]
    proba = svm_model.predict_proba(X_val_scaled[idx].reshape(1, -1))[0]
    confiance = max(proba)
    print(f"   Échantillon {i+1}: Vrai={vrai}, Prédit={pred} (confiance: {confiance:.3f})")

# ============================================
# 9. RÉSUMÉ FINAL
# ============================================
print("\n" + "="*50)
print("🎉 ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS !")
print("="*50)
print(f"📊 RÉSULTATS:")
print(f"   - Précision sur validation: {accuracy:.4f}")
print(f"   - Nombre de classes: {len(np.unique(y_val))}")
print(f"   - Taille du modèle: {svm_model.n_support_.sum()} vecteurs de support")
print(f"\n📁 Fichiers générés:")
print(f"   - svm_model.pkl (le modèle entraîné)")
print(f"   - scaler.pkl (le normalisateur)")
print(f"   - confusion_matrix.png (la matrice de confusion)")
print("="*50)