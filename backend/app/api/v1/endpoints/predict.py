from fastapi import APIRouter

router = APIRouter()

@router.post("/predict")
def predict_sena():
    # Respuesta simulada por ahora 
    return {
        "seña": "Hola",
        "confianza": 0.94,
        "categoria": "Saludo"
    }