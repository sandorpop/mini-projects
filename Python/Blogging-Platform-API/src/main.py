from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)

@app.get("/")
def root():
    return {"message": "Blogging Platform API"}