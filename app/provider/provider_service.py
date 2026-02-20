from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.provider.provider_model import Provider
from app.provider.provider_schema import ProviderBase, ProviderUpdate
from app.user.user_model import User
from app.provider import provider_db
from app.core.errors import AlreadyExistsError, ResourceNotFoundError, ForbiddenError

# Create a new provider
def create_provider(db: Session, current_user: User, provider: ProviderBase) -> Provider:
    # Check name unicity
    existing_provider = provider_db.get_provider_by_name(db, current_user.id, provider.name)
    if existing_provider:
        raise AlreadyExistsError(message="Nom de fournisseur déjà utilisé")
    provider_to_create = Provider(
        **provider.model_dump(),
        user_id = current_user.id
    )
    return provider_db.create_provider(db, provider_to_create)

# Get all providers - filtered by current user
def get_all_providers(db: Session, current_user: User, page: int, page_size: int, name: str = "") -> list[Provider]:
    offset = (page - 1) * page_size
    return provider_db.get_all_providers(db, current_user.id, name, limit=page_size, offset=offset)

# Get one provider by its id - filtered by current user
def get_provider_by_id(db: Session, current_user: User, provider_id: int) -> Provider:
    provider = provider_db.get_provider_by_id(db, current_user.id, provider_id)
    if not provider:
        raise ResourceNotFoundError(message=f"Fournisseur {provider_id} inconnu")
    
    return provider

# Get an existing provider by its name - filtered by current user
def get_provider_by_name(db: Session, current_user: User, name: str) -> Provider:
    provider = provider_db.get_provider_by_name(db, current_user.id, name)
    if not provider:
        raise ResourceNotFoundError(message=f"Fournisseur '{name}' inconnu")
    return provider

# Update an existing provider
def update_provider(db: Session, current_user: User, provider_id: int, updates: ProviderUpdate) -> Provider:
    provider = get_provider_by_id(db, current_user, provider_id)
    
    # Check if user can update this provider
    if current_user.id != provider.user_id:
        raise ForbiddenError(message="Vous ne pouvez pas modifier ce fournisseur.")
    
    if updates.name:
        existing_provider = provider_db.get_provider_by_name(db, current_user.id, updates.name)
        if existing_provider and existing_provider.id != provider.id:
            raise AlreadyExistsError(message="Il existe déjà un fournisseur avec ce nom")
   
    update_data = updates.model_dump(exclude_unset=True)
     
    return provider_db.update_provider(db, provider, update_data)

# Delete an existing provider
def delete_provider(db: Session, current_user: User, provider_id: int):
    provider = get_provider_by_id(db, current_user, provider_id)
    
    # Check if user can delete this provider
    if current_user.id != provider.user_id:
        raise ForbiddenError(message="Vous ne pouvez pas supprimer ce fournisseur.")

    return provider_db.delete_provider(db, provider)
