import os
import joblib
import numpy as np
from app.services.features import normalizar_landmarks

# Definir la ruta absoluta donde se almacena el modelo entrenado
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "..", "ml_models", "modelo_lenguaje_senas.pkl")

# Cargar el modelo entrenado al iniciar el servicio
if os.path.exists(MODEL_PATH):
    modelo = joblib.load(MODEL_PATH)
else:
    modelo = None

def predecir_sena(landmarks):
    """
    Recibe los landmarks en bruto extraídos por MediaPipe,
    aplica la normalización geométrica, redimensiona el arreglo
    y realiza la predicción con el modelo de Machine Learning.
    """
    if modelo is None:
        raise RuntimeError("El modelo de lenguaje de señas no ha sido entrenado o no se encuentra en la ruta especificada.")

    # 1. Aplicar la normalización de landmarks (invariancia a posición y escala)
    landmarks_normalizados = normalizar_landmarks(landmarks)

    # 2. Reshape a formato de 1 sola muestra (1, -1) requerido por scikit-learn
    entrada = np.array(landmarks_normalizados, dtype=float).reshape(1, -1)

    # 3. Realizar la predicción de la clase y la probabilidad (confianza)
    prediccion = modelo.predict(entrada)[0]
    
    # Obtener la probabilidad máxima de la predicción de las clases
    probabilidades = modelo.predict_proba(entrada)
    confianza = float(np.max(probabilidades))

    return prediccion, confianza