from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# URL de conexión a PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_pL9yBCvXeh5H@ep-mute-brook-apt3s1gv-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

# Crear el motor de base de datos
engine = create_engine(DATABASE_URL)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()


class Deposit(Base):
    """Modelo de depósito para la base de datos."""
    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    person = Column(String, nullable=False)  # "Jessica", "Kleeders", "Ambos"
    amount = Column(Float, nullable=False)
    timestamp = Column(String, nullable=False)  # Formato: "YYYY-MM-DD HH:MM:SS"

    def to_dict(self):
        """Convierte el modelo a diccionario para serialización JSON."""
        return {
            "person": self.person,
            "amount": self.amount,
            "timestamp": self.timestamp
        }


# Función para inicializar la base de datos
def init_db():
    """Crea todas las tablas si no existen."""
    Base.metadata.create_all(bind=engine)


# Función para obtener una sesión de base de datos
def get_db():
    """Generador de sesiones para uso en endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
