import os
import joblib
import numpy as np

MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "ml_models", "modelo_lenguaje_senas.pkl"
)

_model = None


def cargar_modelo():
    """Carga el modelo en memoria utilizando lazy loading."""
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"No se encontró el archivo del modelo en la ruta: {MODEL_PATH}"
            )
        _model = joblib.load(MODEL_PATH)
    return _model


def predecir_sena(landmarks: list):
    """Devuelve (clase, confianza) para un vector de 63 landmarks[cite: 8]."""
    model = cargar_modelo()
    entrada = np.array(landmarks).reshape(1, -1)

    # Calcular probabilidades de las clases del modelo
    probabilidades = model.predict_proba(entrada)[0]
    indice = int(np.argmax(probabilidades))

    return str(model.classes_[indice]), float(probabilidades[indice])