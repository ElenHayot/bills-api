from fastapi import FastAPI
from app.core.database import Base, engine

from app.models import user

app = FastAPI(title="Bills API")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def healthcheck():
    return {"status": "ok"}
