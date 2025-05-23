from fastapi import APIRouter, Depends
from app.routes.auth import get_current_user

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/")
def list_students(current_user=Depends(get_current_user)):
    return [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]