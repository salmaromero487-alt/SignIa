from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.models import dataset_master
from app.api.v1.endpoints import predict

# Crear tablas en la base de datos al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SignIA API")

# Configuración de CORS para permitir peticiones desde React (Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas de predicción
app.include_router(predict.router, prefix="/api/v1", tags=["Predicción"])

@app.get("/")
def root():
    return {"status": "Backend de SignIA conectado exitosamente a PostgreSQL"}


    