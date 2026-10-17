import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# 1. Definir la ruta donde se guardará el modelo
MODEL_DIR = os.path.join(os.path.dirname(__file__), "app", "ml_models")
MODEL_PATH = os.path.join(MODEL_DIR, "modelo_lenguaje_senas.pkl")


def generar_y_guardar_modelo():
    # Crear el directorio si no existe
    os.makedirs(MODEL_DIR, exist_ok=True)

    print("Generando estructura base del modelo de ML...")

    # Crear datos sintéticos de muestra con la forma exacta (63 características por mano)
    # 26 clases representando las letras del abecedario
    clases = [chr(i) for i in range(ord("A"), ord("Z") + 1)]

    X_dummy = []
    y_dummy = []

    # Generar muestras simuladas para cada clase para inicializar el estimador
    np.random.seed(42)
    for clase in clases:
        for _ in range(10):  # 10 ejemplos por clase
            # 63 valores flotantes simulando las coordenadas (x, y, z) normalizadas de MediaPipe
            landmarks_simulados = np.random.uniform(0.0, 1.0, 63)
            X_dummy.append(landmarks_simulados)
            y_dummy.append(clase)

    X_dummy = np.array(X_dummy)
    y_dummy = np.array(y_dummy)

    # 2. Inicializar y entrenar el modelo Random Forest
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_dummy, y_dummy)

    # 3. Guardar el modelo en disco (.pkl)
    joblib.dump(clf, MODEL_PATH)
    print(f" ¡Modelo generado y guardado exitosamente en: {MODEL_PATH}!")


if __name__ == "__main__":
    generar_y_guardar_modelo()