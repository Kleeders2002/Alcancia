from fastapi import FastAPI, HTTPException, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from models import Deposit, get_db, init_db
from sqlalchemy.orm import Session
from sqlalchemy import text

app = FastAPI(title="🐷 Alcancía Virtual")

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción podrías restringirlo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar la base de datos al iniciar la aplicación
@app.on_event("startup")
def startup_event():
    """Inicializa la base de datos al iniciar la aplicación."""
    init_db()

# ----------------------------
# Modelos Pydantic
# ----------------------------
class DepositResponse(BaseModel):
    success: bool
    message: Optional[str] = None

class DepositCreate(BaseModel):
    person: str
    amount: float

# ----------------------------
# Endpoints de la API
# ----------------------------
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Endpoint de health check para verificar que todo funciona correctamente."""
    try:
        # Verificar conexión a la base de datos
        db.execute(text("SELECT 1"))
        db.commit()
        return {
            "status": "healthy",
            "database": "connected",
            "message": "✅ Todo funcionando correctamente"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "message": f"❌ Error: {str(e)}"
        }, 500

@app.get("/api/deposits")
async def get_deposits(db: Session = Depends(get_db)):
    """Devuelve todos los depósitos desde PostgreSQL."""
    deposits = db.query(Deposit).all()
    return [deposit.to_dict() for deposit in deposits]

@app.post("/api/deposits", response_model=DepositResponse)
async def add_deposit(person: str = Form(...), amount: float = Form(...), db: Session = Depends(get_db)):
    """Añade un nuevo depósito a PostgreSQL."""
    # Validaciones
    if person not in ["Jessica", "Kleeders", "Ambos"]:
        raise HTTPException(status_code=400, detail="Persona no válida")
    if amount <= 0 or amount > 100000:
        raise HTTPException(status_code=400, detail="Monto inválido")

    # Crear depósito en base de datos
    new_deposit = Deposit(
        person=person,
        amount=amount,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.add(new_deposit)
    db.commit()
    db.refresh(new_deposit)

    return {"success": True, "message": "Depósito agregado correctamente"}

# ----------------------------
# Servir archivos estáticos (el frontend)
# ----------------------------
# Montamos la carpeta actual para que sirva index.html, style.css, script.js
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def root():
    """Sirve la página principal."""
    return FileResponse("index.html")

@app.delete("/api/deposits/{index}", response_model=DepositResponse)
async def delete_deposit(index: int, db: Session = Depends(get_db)):
    """Elimina un depósito por su índice."""
    # Obtener todos los depósitos ordenados por timestamp (más antiguo primero)
    deposits = db.query(Deposit).order_by(Deposit.id).all()

    if index < 0 or index >= len(deposits):
        raise HTTPException(status_code=404, detail="Depósito no encontrado")

    # Eliminar el depósito en el índice especificado
    deposit_to_delete = deposits[index]
    db.delete(deposit_to_delete)
    db.commit()

    return {"success": True, "message": "Depósito eliminado"}