from fastapi import FastAPI
from . import models
from .database import engine
from .routers import auth, exercises, workouts, reports

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(exercises.router)
app.include_router(workouts.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "Workout Tracker API"}