from fastapi import FastAPI
from app.routes import auth, students
from app.database import Base, engine
from app import models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="SbappyTrack API")

app.include_router(auth.router)
app.include_router(students.router)

@app.get("/")
def read_root():
    return {"msg": "SbappyTrack API online"}