from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

# Configuração do SQLite com caminho absoluto
BASE_DIR = Path(__file__).parent
SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR/'sbappy.db'}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,  # Mostra SQL no console (útil para desenvolvimento)
    pool_pre_ping=True  # Verifica se conexão está ativa antes de usar
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Melhora desempenho
)

Base = declarative_base()

def get_db():
    """
    Fornece uma sessão de banco de dados para cada requisição.
    Fecha automaticamente após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()