import datetime
 
from app.db.database import Base
from sqlalchemy import Column, DateTime, Float, Integer, String
 
 
class RegistroPrediccion(Base):
    __tablename__ = "registro_predicciones"
 
    id = Column(Integer, primary_key=True, index=True)
    glosa_predicha = Column(String)
    confianza = Column(Float)
    fecha = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
