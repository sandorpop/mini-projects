from fastapi import FastAPI
from .routers import auth, exercises, workouts, reports

app = FastAPI(
    title="Workout Tracker API",
    description="A REST API for tracking workouts, exercises, and progress.",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(exercises.router)
app.include_router(workouts.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "Workout Tracker API"}