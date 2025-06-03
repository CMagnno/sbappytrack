from fastapi import FastAPI, Depends, HTTPException
from app.routes import auth, students
from app.database import SessionLocal, engine, Base
from app.models import User, Student, Submission  # Importe todos os modelos
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import os

app = FastAPI(
    title="SbappyTrack API",
    description="API para gerenciamento de estudantes e submissões de código",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração de rotas
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(students.router, prefix="/api/v1", tags=["Students"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependência de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Status"])
def read_root():
    return {
        "message": "SbappyTrack API online",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.on_event("startup")
async def startup_db():
    # Verifique se o banco de dados existe e delete se necessário
    if os.path.exists("./sbappy.db"):
        try:
            os.remove("./sbappy.db")
            print("🗑️ Banco de dados antigo removido")
        except Exception as e:
            print(f"⚠️ Erro ao remover banco antigo: {e}")

    # Crie todas as tabelas
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso")

    # Popule dados iniciais
    await populate_initial_data()

async def populate_initial_data():
    db = SessionLocal()
    try:
        # Crie usuário admin se não existir
        if not db.query(User).first():
            admin = User(
                username="admin",
                email="admin@example.com",
                hashed_password=pwd_context.hash("admin123")
            )
            db.add(admin)
            db.commit()
            print("✅ Usuário admin criado com sucesso")

        # Adicione outros dados iniciais se necessário
        if not db.query(Student).first():
            sample_student = Student(
                name="Aluno Exemplo",
                course="Ciência da Computação"
            )
            db.add(sample_student)
            db.commit()
            print("✅ Aluno exemplo criado com sucesso")

    except Exception as e:
        print(f"❌ Erro ao popular dados iniciais: {e}")
        db.rollback()
    finally:
        db.close()