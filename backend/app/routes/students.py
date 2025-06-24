
import subprocess

from app import database, models, schemas
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/students", tags=["Students"])

class CodeInput(BaseModel):
    code: str

@router.post("/submit")
def submit_code(payload: CodeInput):
    try:
        result = subprocess.run(
            ["python3", "-c", payload.code],
            text=True,
            capture_output=True,
            timeout=5
        )
        return {
            "output": result.stdout,
            "error": result.stderr
        }
    except Exception as e:
        return {"error": str(e)}

