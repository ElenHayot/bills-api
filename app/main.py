from fastapi import FastAPI
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

from app.models import user
from app.routers.auth import auth_router
from app.routers.user import user_router

app = FastAPI(title="Bills API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_VERSION = "v1"

app.include_router(auth_router, prefix=f"/api/{API_VERSION}/auth")
app.include_router(user_router, prefix=f"/api/{API_VERSION}/users")

def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)


@app.get("/")
def healthcheck():
    return {"status": "ok"}
