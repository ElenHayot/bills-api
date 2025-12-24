#Fichier de configuration des tests unitaires (chargé automatiquement par pytest)
import pytest     #Pour créer des "fixtures"
from fastapi.testclient import TestClient   #permet de simuler des requêtes http
from sqlalchemy import create_engine    #création d'une base SQLAlchemy pour les tests
from sqlalchemy.orm import sessionmaker #création d'une base SQLAlchemy pour les tests
from sqlalchemy.pool import StaticPool  # Pour SQLite en mémoire

from app.core.database import Base, get_db        #Base des modèles SQLAlchemy pour créer/supprimer des tables
from app.main import app                #Application FastAPI

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},  #pour pouvoir utiliser depuis le TestClient
    poolclass=StaticPool,  # Utilise la même connexion pour tout
    #echo=True  # Pour débugger (à enlever plus tard)
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Remplace la db de l'API par une qui pointe vers la db_test
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

        #**** 3. Override de la dépendance et client de test ****#
@pytest.fixture(scope="function")
def client():
    # Pour débugger
    print("Tables connues par Base:", list(Base.metadata.tables.keys()))
    
    Base.metadata.create_all(bind=engine)   # créer toutes les tables pour les tests
    
    # Pour débuguer : Vérifier que les tables sont bien créées sur le bon engine
    from sqlalchemy import inspect
    inspector = inspect(engine)
    print("Tables réellement créées sur notre engine:", inspector.get_table_names())
    
    # Surcharge la dépendance durant les tests pour rediriger les routes vers la db_test
    app.dependency_overrides[get_db] = override_get_db
    
    # Pour débuguer : Tester la dépendance
    test_db = next(override_get_db())
    print("Engine utilisé par override:", test_db.bind.url)
    test_db.close()

    with TestClient(app) as test_client:
        yield test_client                   # on donne un client prêt à tester
   
    app.dependency_overrides.clear()        #nettoyage de la dépendance
    Base.metadata.drop_all(bind=engine)     # on efface tout après chaque test
