import argparse
import os
import pandas as pd

parser = argparse.ArgumentParser(description="Normalize and standardize a CSV dataset.")
parser.add_argument("csv_path", nargs="?", default="bldc_predictive_maintenance_dataset (1) (1) (1).csv", help="Path to input CSV file (default: bldc_predictive_maintenance_dataset (1) (1) (1).csv)")
args = parser.parse_args()

file_path = args.csv_path
if not os.path.isfile(file_path):
    raise FileNotFoundError(
        f"Input file not found: {file_path}\nPlease provide a valid CSV path. Example: python normalizationEtstandar.py train_data.csv"
    )

df = pd.read_csv(file_path)
print(df.head())
print(df.info())



#featurs



target_column = "Fault_Label"   # <-- à modifier si nécessaire

X = df.drop(columns=[target_column])
y = df[target_column]



#normalization entre -1 et 1




from sklearn.preprocessing import MinMaxScaler

scaler_neg1_1 = MinMaxScaler(feature_range=(-1, 1))

X_normalized = scaler_neg1_1.fit_transform(X)

X_normalized = pd.DataFrame(X_normalized, columns=X.columns)

print("Normalisation [-1,1] :")
print(X_normalized.head())
X_normalized[target_column] = y
X_normalized.to_csv("dataset_normalized.csv", index=False)

#standardisation


from sklearn.preprocessing import StandardScaler

scaler_standard = StandardScaler()

X_standardized = scaler_standard.fit_transform(X)

X_standardized = pd.DataFrame(X_standardized, columns=X.columns)

print("Standardisation :")
print(X_standardized.head())

X_standardized[target_column] = y
X_standardized.to_csv("dataset_standardized.csv", index=False)


import joblib

# ... après avoir fait le fit_transform ...
joblib.dump(scaler_standard, 'scaler.pkl')
print("Scaler sauvegardé sous 'scaler.pkl'")

#test

print("Min après normalisation :", X_normalized.min().min())
print("Max après normalisation :", X_normalized.max().max())

print("Moyenne après standardisation :")
print(X_standardized.mean())

print("Ecart-type après standardisation :")
print(X_standardized.std())