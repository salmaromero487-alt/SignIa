from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db.database import Base
import datetime

class DatasetMuestra(Base):
    __tablename__ = "dataset_master"

    id = Column(Integer, primary_key=True, index=True)
    glosa = Column(String)
    categoria = Column(String)
    confianza = Column(Float)
    fecha_captura = Column(DateTime, default=datetime.datetime.utcnow)