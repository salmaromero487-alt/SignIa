import os
import sys
import csv
import json
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import LeaveOneGroupOut, cross_val_score

# Asegurar la ruta para importar los servicios del backend
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))
from services.features import normalizar_landmarks

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "labels", "dataset_master.csv")
MODEL_DIR = os.path.join(BASE_DIR, "app", "ml_models")
MODEL_PATH = os.path.join(MODEL_DIR, "modelo_lenguaje_senas.pkl")

def cargar_datos():
    X, y, personas = [], [], []
    if not os.path.exists(CSV_PATH):
        print(f"No se encontró el archivo CSV en: {CSV_PATH}")
        return np.array(X), np.array(y), np.array(personas)
        
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            ruta_relativa = fila["ruta_archivo"]
            # Ajustar la ruta absoluta al archivo json de la muestra
            ruta_json = os.path.abspath(os.path.join(BASE_DIR, "..", "data", ruta_relativa))
            
            if not os.path.exists(ruta_json):
                continue
            with open(ruta_json, encoding="utf-8") as g:
                datos = json.load(g)
                
            X.append(normalizar_landmarks(datos["landmarks"]))
            y.append(fila["glosa"])
            personas.append(fila["persona_id"])
            
    return np.array(X), np.array(y), np.array(personas)

def main():
    print("Cargando muestras reales para entrenamiento...")
    X, y, personas = cargar_datos()
    
    if len(y) == 0:
        print("No hay muestras disponibles para entrenar. Captura datos primero.")
        return
        
    print(f"Muestras cargadas: {len(y)} | Clases (Señas): {len(set(y))} | Participantes únicos: {len(set(personas))}")
    
    if len(set(personas)) < 2:
        print("Advertencia: Se recomienda tener muestras de al menos 2 o 3 personas distintas para una validación robusta con LeaveOneGroupOut.")

    # Inicializar clasificador de Random Forest
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    
    # Validación cruzada Leave One Group Out (agrupada por persona_id)
    if len(set(personas)) >= 2:
        logo = LeaveOneGroupOut()
        puntajes = cross_val_score(clf, X, y, groups=personas, cv=logo)
        print("Exactitud por cada persona dejada fuera:", np.round(puntajes, 3))
        print(f"Exactitud media general (Generalización): {puntajes.mean():.3f}")

    # Entrenar con el 100% de los datos recolectados y guardar el modelo
    clf.fit(X, y)
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print(f" ¡Modelo entrenado con éxito y guardado en: {MODEL_PATH}!")

if __name__ == "__main__":
    main()