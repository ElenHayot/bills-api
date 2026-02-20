from fastapi import FastAPI
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

from app.user import user_model
from app.auth.auth_router import auth_router
from app.user.user_router import user_router
from app.category.category_router import category_router
from app.bill.bill_router import bill_router
from app.dashboard.dashboard_router import dashboard_router
from app.provider.provider_router import provider_router

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
app.include_router(category_router, prefix=f"/api/{API_VERSION}/categories")
app.include_router(bill_router, prefix=f"/api/{API_VERSION}/bills")
app.include_router(dashboard_router,prefix=f"/api/{API_VERSION}/dashboard")
app.include_router(provider_router, prefix=f"/api/{API_VERSION}/providers")

def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)


@app.get("/")
def healthcheck():
    return {"status": "ok"}
