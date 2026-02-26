"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import os

from app.core.database import Base, engine
from app.core.settings import settings

from app.user import user_model
from app.auth.auth_router import auth_router
from app.user.user_router import user_router
from app.category.category_router import category_router
from app.bill.bill_router import bill_router
from app.dashboard.dashboard_router import dashboard_router
from app.provider.provider_router import provider_router

# Middleware pour les headers de sécurité
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Protection contre XSS
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Sécurité HTTPS (uniquement en production)
        if os.getenv("ENVIRONMENT") == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            response.headers["Expect-CT"] = "max-age=86400"
        
        # Politique de sécurité de contenu
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        # Référenceur
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response

app = FastAPI(title=settings.app_name,
              description=settings.app_description,
              version=settings.version,
              contact={"name": "Elen Hayot", "email": "elen.hayot@gmail.com"},
              license_info={"name": "MIT License"})

# Configuration CORS via variables d'environnement
#allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:8081,http://localhost:5432").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)

# Ajouter les headers de sécurité
app.add_middleware(SecurityHeadersMiddleware)

# Hôtes de confiance (uniquement en production)
if settings.environment == "production" or settings.environment == "staging":
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts.split(","))
    
    # Forcer HTTPS en production
    app.add_middleware(HTTPSRedirectMiddleware)

API_PREFIX = f"{settings.url_prefix}/{settings.url_version}"

app.include_router(auth_router, prefix=f"{API_PREFIX}/auth")
app.include_router(user_router, prefix=f"{API_PREFIX}/users")
app.include_router(category_router, prefix=f"{API_PREFIX}/categories")
app.include_router(bill_router, prefix=f"{API_PREFIX}/bills")
app.include_router(dashboard_router,prefix=f"{API_PREFIX}/dashboard")
app.include_router(provider_router, prefix=f"{API_PREFIX}/providers")

def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)


@app.get("/")
def healthcheck():
    return {"status": "ok"}
