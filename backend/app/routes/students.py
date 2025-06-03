# app/routes/students.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/", response_model=list[schemas.StudentOut])
def list_students(db: Session = Depends(database.get_db)):
    return db.query(models.Student).all()

@router.post("/", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student
