import cv2
import numpy as np
import mediapipe as mp

def extraer_landmarks(image_bytes: bytes):
    if not image_bytes:
        return None

    try:
        # Importación directa de la solución de manos
        mp_hands = mp.solutions.hands
        
        # Cargar imagen desde bytes
        np_img = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if frame is None:
            return None

        # Convertir BGR a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Inicializar el detector
        with mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.1
        ) as hands:
            
            # Intento 1: Imagen completa
            results = hands.process(rgb_frame)

            # Intento 2: Si no la encuentra, recortar la mitad superior izquierda (donde suele estar la mano)
            if not results.multi_hand_landmarks:
                h, w = frame.shape[:2]
                crop = frame[0:int(h*0.85), 0:int(w*0.6)]
                if crop.size > 0:
                    crop_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
                    results = hands.process(crop_rgb)

            if not results.multi_hand_landmarks:
                return None

            # Extraer las 63 coordenadas (21 puntos x 3 ejes)
            landmarks = []
            for lm in results.multi_hand_landmarks[0].landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            return landmarks

    except Exception as e:
        print(f"Error en extraer_landmarks: {e}")
        return None