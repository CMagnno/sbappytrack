from pydantic import BaseModel, EmailStr
from typing import Optional

# === AUTHENTICATION ===

class UserCreate(BaseModel):
    username: str
    email: EmailStr  # Mantendo o EmailStr do segundo arquivo
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr  # Adicionando email que estava no segundo arquivo

    class Config:
        from_attributes = True  # Padronizando para Pydantic v2

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# === SUBMISSIONS ===

class SubmissionCreate(BaseModel):
    code: str
    exercise_id: int

class SubmissionOut(BaseModel):
    id: int
    output: str
    error: str
    time: int

    class Config:
        from_attributes = True  # Padronizando para Pydantic v2

# === STUDENTS ===

class StudentBase(BaseModel):
    name: str
    course: str

class StudentCreate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int

    class Config:
        from_attributes = True