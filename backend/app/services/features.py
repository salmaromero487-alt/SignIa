import numpy as np

def normalizar_landmarks(landmarks):
    """
    Hace el vector de landmarks invariante a posición y escala.
    Resta la posición de la muñeca (landmark 0) y divide entre la distancia máxima.
    """
    puntos = np.array(landmarks, dtype=float).reshape(21, 3)
    puntos = puntos - puntos[0]  # Centrar en la muñeca
    escala = np.max(np.linalg.norm(puntos, axis=1))
    if escala > 0:
        puntos = puntos / escala
    return puntos.flatten()