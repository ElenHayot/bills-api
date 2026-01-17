from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.provider import Provider

# Get all providers
def get_all_providers(db: Session, user_id: int, name: str = "", limit: int = None, offset: int = None) -> list[Provider]:
    query = select(Provider).order_by(Provider.name.asc())
    query = query.where(Provider.user_id == user_id)

    if name:
        query = query.where(Provider.name.ilike(f"%{name}%"))

    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
        
    providers = db.execute(query)
    return providers.scalars().all()

# Find a provider by its id and user_id
def get_provider_by_id(db: Session, user_id: int, id: int) -> Provider:
    provider = db.execute(select(Provider).where(Provider.user_id == user_id, Provider.id == id))
    return provider.scalar_one_or_none()

# Find a provider by its name and user_id
def get_provider_by_name(db: Session, user_id: int, name: str) -> Provider:
    provider = db.execute(select(Provider).where(Provider.user_id == user_id, Provider.name == name))
    return provider.scalar_one_or_none()

# Add a new provider in db
def create_provider(db: Session, db_provider: Provider) -> Provider:
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

# Update an existing provider in db
def update_provider(db: Session, provider: Provider, updates: dict) -> Provider:
    for key, value in updates.items():
        if hasattr(provider, key):  # petit garde-fou si mauvaise key
            setattr(provider, key, value)

    db.commit()
    db.refresh(provider)
    return provider

# Remove a provider from db
def delete_provider(db: Session, provider: Provider):
    db.delete(provider)
    db.commit()