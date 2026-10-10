from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cadena con tu usuario y contraseña real
DATABASE_URL = "postgresql://postgres:admin2026@localhost:5432/signia_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()