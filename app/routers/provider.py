from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.provider import ProviderBase, ProviderRead, ProviderUpdate
from app.dependencies.auth import get_current_user
from app.services import provider_service

provider_router = APIRouter(tags=["Providers"])

# POST : Create a provider for the current user
@provider_router.post("/", response_model=ProviderRead,
                    summary="Create a provider for the current user")
def create(provider_data: ProviderBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return provider_service.create_provider(db, current_user, provider_data)

# GET : get all current user's providers
@provider_router.get("/", response_model=list[ProviderRead],
                    summary="Providers data for the current user",
                    description="Returns all current user's providers")
def read_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), 
             page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), 
             name: str = Query(None)):
    return provider_service.get_all_providers(db, current_user, page, page_size, name)

# GET : Get one provider by its name, filtered by current user
@provider_router.get("/{provider_id}/", response_model=ProviderRead,
                    summary="Provider data for a given provider ID")
def read(provider_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return provider_service.get_provider_by_id(db, current_user, provider_id)

# PUT : Update a current user's provider
@provider_router.put("/{provider_id}/", response_model=ProviderRead,
                    summary="Update a provider",
                    description="Update an existing provider - returns the updated data")
def update(provider_id: int, updates: ProviderUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return provider_service.update_provider(db, current_user, provider_id, updates)

# DELETE : Delete a provider from the current user
@provider_router.delete("/{provider_id}/",
                    summary="Delete a provider",
                    description="Delete an existing provider - returns nothing")
def delete(provider_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return provider_service.delete_provider(db, current_user, provider_id)