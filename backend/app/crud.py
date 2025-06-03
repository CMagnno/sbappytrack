from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,  # Adicionando o campo email que estava faltando
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        # Tentar autenticar por email também
        user = get_user_by_email(db, username)
        if not user:
            return False
    
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_submission(db: Session, user_id: int, submission: schemas.SubmissionCreate, result: dict):
    db_submission = models.Submission(
        code=submission.code,
        output=result.get("output", ""),
        error=result.get("error", ""),
        time=result.get("time", 0),
        user_id=user_id,
        exercise_id=submission.exercise_id
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

# Adicionando operações CRUD para estudantes
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        name=student.name,
        course=student.course
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()