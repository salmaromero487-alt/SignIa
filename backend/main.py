from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.models import dataset_master
from app.api.v1.endpoints import predict

# Instrucción para que SQLAlchemy cree la tabla en PostgreSQL al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SignIA API")

app.include_router(predict.router, prefix="/api/v1", tags=["Predicción"])

# Habiliatr CORS parapermitir peticiones desde el Ract (Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas con el prefijo correcto
app.include_router(predict.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"status": "Backend de SignIA conectado exitosamente a PostgreSQL"}