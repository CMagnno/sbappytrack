# app/routes/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, auth

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    dependencies=[Depends(auth.get_current_user)]
)

@router.get("/")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Estatísticas básicas
    stats = {
        "total_students": db.query(models.Student).count(),
        "total_submissions": db.query(models.Submission).count(),
        "common_errors": []  # Implementar lógica de análise
    }
    return stats