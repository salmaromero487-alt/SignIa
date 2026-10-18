"""Entrena el clasificador con las muestras reales de data/.
Evalúa dejando una persona fuera cada vez (LeaveOneGroupOut)."""
import csv
import json
import os
import sys
 
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import LeaveOneGroupOut, cross_val_score
 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.services.features import normalizar_landmarks  # noqa: E402
 
BASE = os.path.join(os.path.dirname(__file__), "..", "..")
RAIZ_DATA = os.path.join(BASE, "data")
CSV_PATH = os.path.join(RAIZ_DATA, "labels", "dataset_master.csv")
MODEL_PATH = os.path.join(BASE, "backend", "app", "ml_models", "modelo_lenguaje_senas.pkl")
 
 
def cargar():
    X, y, personas = [], [], []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            ruta = os.path.join(RAIZ_DATA, fila["ruta_archivo"])
            if not os.path.exists(ruta):
                continue
            with open(ruta, encoding="utf-8") as g:
                datos = json.load(g)
            X.append(normalizar_landmarks(datos["landmarks"]))
            y.append(fila["glosa"])
            personas.append(fila["persona_id"])
    return np.array(X), np.array(y), np.array(personas)
 
 
def main():
    X, y, personas = cargar()
    print(f"Muestras: {len(y)} | Clases: {len(set(y))} | Personas: {len(set(personas))}")
    if len(set(personas)) < 3:
        print("Se necesitan al menos 3 personas para evaluar con una persona fuera.")
        return
 
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    puntajes = cross_val_score(clf, X, y, groups=personas, cv=LeaveOneGroupOut())
    print("Exactitud por persona dejada fuera:", np.round(puntajes, 3))
    print(f"Exactitud media: {puntajes.mean():.3f}")
 
    clf.fit(X, y)
    joblib.dump(clf, MODEL_PATH)
    print(f"Modelo guardado en: {MODEL_PATH}")
 
 
if __name__ == "__main__":
    main()
