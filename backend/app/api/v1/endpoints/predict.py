from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.config import UMBRAL_CONFIANZA
from app.db.database import get_db
from app.models.dataset_master import DatasetMuestra
from app.services.ml_service import predecir_sena
from app.services.vision_service import extraer_landmarks

router = APIRouter()


@router.post("/predict")
async def predict_sena(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    contents = await file.read()
    landmarks = extraer_landmarks(contents)

    if landmarks is None:
        raise HTTPException(
            status_code=400,
            detail="No se pudo detectar ninguna mano en la imagen enviada.",
        )

    try:
        clase, confianza = predecir_sena(landmarks)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la predicción con el modelo de ML: {str(e)}",
        )

    # Flujo alternativo A (RF07): confianza por debajo del umbral, no se persiste
    if confianza < UMBRAL_CONFIANZA:
        return {
            "status": "low_confidence",
            "prediction": None,
            "confidence": round(confianza, 4),
            "message": "Seña no reconocida, repita el gesto",
        }

    # Camino feliz (RF06): se persiste la muestra en la base de datos
    muestra = DatasetMuestra(
        glosa=clase, categoria="sin_categoria", confianza=confianza
    )
    db.add(muestra)
    db.commit()

    return {
        "status": "success",
        "prediction": clase,
        "confidence": round(confianza, 4),
        "landmarks_count": len(landmarks),
    }