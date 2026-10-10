"""Captura de muestras del dataset SignIA (un fotograma por muestra).
Controles: ESPACIO = guardar muestra | N = siguiente seña | Q = salir
"""

import csv
import json
import os
import sys
from datetime import datetime
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.services.vision_service import extraer_landmarks  # noqa: E402

VOCABULARIO = {
    "Saludo": ["Hola", "Buenos dias", "Buenas tardes", "Buenas noches", "Adios"],
    "Cortesia": ["Gracias", "Por favor", "De nada", "Perdon", "Si", "No"],
    "Necesidades basicas": ["Agua", "Comida", "Bano", "Dormir", "Ayuda"],
    "Preguntas comunes": ["Como estas", "Como te llamas", "Donde esta", "Que hora es"],
    "Emergencia": ["Emergencia", "Dolor", "Medico", "Policia", "Fuego"],
}

RAIZ_DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
CSV_PATH = os.path.join(RAIZ_DATA, "labels", "dataset_master.csv")

CAMPOS = [
    "id_muestra",
    "glosa",
    "categoria",
    "subcategoria",
    "tipo_sena",
    "mano_dominante",
    "duracion_frames",
    "persona_id",
    "repeticion",
    "condiciones_captura",
    "formato",
    "ruta_archivo",
    "licencia_fuente",
    "validado_por",
]


def siguiente_repeticion(glosa, persona_id):
    if not os.path.exists(CSV_PATH):
        return 1
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        previas = [
            r
            for r in csv.DictReader(f)
            if r["glosa"] == glosa and r["persona_id"] == persona_id
        ]
    return len(previas) + 1


def total_muestras():
    if not os.path.exists(CSV_PATH):
        return 0
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return sum(1 for _ in csv.DictReader(f))


def guardar_muestra(frame, glosa, categoria, persona_id, mano, condiciones):
    ok, buffer = cv2.imencode(".jpg", frame)
    landmarks = extraer_landmarks(buffer.tobytes()) if ok else None
    if landmarks is None:
        print("  No se detectó mano; muestra descartada.")
        return False

    repeticion = siguiente_repeticion(glosa, persona_id)
    nombre = f"{glosa.replace(' ', '_').lower()}_{persona_id}_r{repeticion}.json"
    carpeta = os.path.join(
        RAIZ_DATA, "processed", categoria.replace(" ", "_").lower()
    )
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, nombre)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump({"glosa": glosa, "landmarks": landmarks}, f)

    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    nuevo = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        if nuevo:
            w.writeheader()
        w.writerow(
            {
                "id_muestra": f"SIG-{total_muestras() + 1:04d}",
                "glosa": glosa,
                "categoria": categoria,
                "subcategoria": "",
                "tipo_sena": "estatica",
                "mano_dominante": mano,
                "duracion_frames": 1,
                "persona_id": persona_id,
                "repeticion": repeticion,
                "condiciones_captura": condiciones,
                "formato": "imagen",
                "ruta_archivo": os.path.relpath(ruta, RAIZ_DATA),
                "licencia_fuente": "Propio",
                "validado_por": "Pendiente",
            }
        )
    print(f"  Guardada: {nombre}")
    return True


def main():
    print(
        "Esta herramienta graba a una persona. ¿Existe consentimiento informado firmado?"
    )
    if input("Escriba SI para continuar: ").strip().upper() != "SI":
        print("Captura cancelada: se requiere consentimiento.")
        return

    persona_id = input("ID anónimo de la persona (ej. P01): ").strip()
    mano = input("Mano dominante (derecha/izquierda): ").strip()
    condiciones = input(
        "Condiciones (ej. interior, fondo neutro, 1.5 m): "
    ).strip()

    lista = [(cat, g) for cat, gs in VOCABULARIO.items() for g in gs]
    indice = 0

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break

        categoria, glosa = lista[indice]
        vista = frame.copy()
        cv2.putText(
            vista,
            f"{glosa} ({categoria}) rep {siguiente_repeticion(glosa, persona_id)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )
        cv2.imshow(
            "SignIA - captura (ESPACIO guarda, N siguiente, Q sale)", vista
        )

        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord(" "):
            guardar_muestra(frame, glosa, categoria, persona_id, mano, condiciones)
        elif tecla == ord("n"):
            indice = (indice + 1) % len(lista)
        elif tecla == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()