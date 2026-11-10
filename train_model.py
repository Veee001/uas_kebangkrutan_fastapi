import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)
import joblib

def main():
    print("1. Memuat dataset 'data.csv'...")
    df = pd.read_csv('data.csv')
    df.columns = df.columns.str.strip()

    selected_features = [
        'ROA(C) before interest and depreciation before interest',
        'Net Income to Total Assets',
        'Debt ratio %',
        'Net worth/Assets',
        'Current Ratio',
        'Quick Ratio',
        'Operating Gross Margin',
        'Cash Flow to Total Assets'
    ]
    target_column = 'Bankrupt?'

    X = df[selected_features]
    y = df[target_column]

    # Split 80% Training, 20% Testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Normalisasi menggunakan StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Training Model Multi-Layer Perceptron (MLPClassifier)
    print("2. Melatih model Multi-Layer Perceptron (MLPClassifier)...")
    mlp_model = MLPClassifier(
        hidden_layer_sizes=(64, 32),
        activation='relu',
        solver='adam',
        max_iter=300,
        random_state=42
    )
    mlp_model.fit(X_train_scaled, y_train)

    # Evaluasi Model (Soal 1b)
    y_pred = mlp_model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred).tolist()

    print("\n=== HASIL EVALUASI MODEL MLP (SOAL 1b) ===")
    print(f"Accuracy  : {acc:.4f} ({acc*100:.2f}%)")
    print(f"Precision : {prec:.4f} ({prec*100:.2f}%)")
    print(f"Recall    : {rec:.4f} ({rec*100:.2f}%)")
    print(f"F1-Score  : {f1:.4f} ({f1*100:.2f}%)")
    print("\nConfusion Matrix:")
    print(np.array(cm))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Sehat (0)', 'Bangkrut (1)']))

    # Simpan Model, Scaler, dan Metrik Evaluasi (Soal 1c)
    joblib.dump(mlp_model, 'model_mlp.pkl')
    joblib.dump(scaler, 'scaler.pkl')

    metrics_data = {
        "accuracy": round(acc * 100, 2),
        "precision": round(prec * 100, 2),
        "recall": round(rec * 100, 2),
        "f1_score": round(f1 * 100, 2),
        "confusion_matrix": cm,
        "total_data": int(len(df)),
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
        "n_iterations": int(mlp_model.n_iter_)
    }
    with open('metrics.json', 'w') as f:
        json.dump(metrics_data, f, indent=4)

    print("\n3. Model berhasil disimpan ke 'model_mlp.pkl', 'scaler.pkl', dan 'metrics.json'!")

if __name__ == '__main__':
    main()
