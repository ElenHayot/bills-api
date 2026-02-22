from unit_tests.datas import (
    URL_AUTH, URL_USERS, URL_CATEGORIES,
    john_doe, login_john_doe, john_doe_category,
    test_category_2, test_category_3
)
import pytest

def get_auth_headers(client, user_data=login_john_doe):
    """Helper pour obtenir les headers d'authentification"""
    response = client.post(
        f"{URL_AUTH}/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=user_data
    )
    return {"Authorization": f"bearer {response.json()['access_token']}"}

def test_create_category(client):
    # Créer et connecter utilisateur
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    assert response.status_code == 200
    headers = get_auth_headers(client)
    
    # Créer category
    response = client.post(URL_CATEGORIES, headers=headers, json=test_category_2)
    assert response.status_code == 200
    category = response.json()
    assert category["name"] == test_category_2["name"]
    assert category["color"] == test_category_2["color"]

def test_get_categories(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    # Créer plusieurs categories
    client.post(URL_CATEGORIES, headers=headers, json=test_category_2)
    client.post(URL_CATEGORIES, headers=headers, json=test_category_3)
    
    # Get categories (devrait inclure la category par défaut)
    response = client.get(URL_CATEGORIES, headers=headers)
    assert response.status_code == 200
    categories = response.json()
    assert len(categories) == 3  # 2 créées + 1 par défaut

def test_get_category_by_id(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    # Créer category
    create_response = client.post(URL_CATEGORIES, headers=headers, json=test_category_2)
    category_id = create_response.json()["id"]
    
    # Get category by id
    response = client.get(f"{URL_CATEGORIES}/{category_id}/", headers=headers)
    assert response.status_code == 200
    category = response.json()
    assert category["id"] == category_id
    assert category["name"] == test_category_2["name"]

def test_update_category(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    # Créer category
    create_response = client.post(URL_CATEGORIES, headers=headers, json=test_category_2)
    category_id = create_response.json()["id"]
    
    # Update category
    update_data = {"name": "Transport Modifié", "color": "red"}
    response = client.put(f"{URL_CATEGORIES}/{category_id}/", headers=headers, json=update_data)
    assert response.status_code == 200
    updated_category = response.json()
    assert updated_category["name"] == "Transport Modifié"
    assert updated_category["color"] == "red"

def test_delete_category(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    # Créer category
    create_response = client.post(URL_CATEGORIES, headers=headers, json=test_category_2)
    category_id = create_response.json()["id"]
    
    # Delete category
    response = client.delete(f"{URL_CATEGORIES}/{category_id}/", headers=headers)
    assert response.status_code == 200
    
    # Vérifier que la category n'existe plus
    response = client.get(f"{URL_CATEGORIES}/{category_id}/", headers=headers)
    assert response.status_code == 404

def test_category_unauthorized_access(client):
    # Test accès sans authentification
    response = client.get(URL_CATEGORIES)
    assert response.status_code == 401
    
    response = client.post(URL_CATEGORIES, json=test_category_2)
    assert response.status_code == 401

def test_category_user_isolation(client):
    # Créer 2 utilisateurs
    response = client.post(URL_USERS, json=john_doe)
    assert response.status_code == 200
    response = client.post(URL_USERS, json={"email": "test2@example.com", "password": "test1234"})
    assert response.status_code == 200

    # Connecter premier utilisateur
    headers1 = get_auth_headers(client, login_john_doe)
    
    # Connecter deuxième utilisateur
    response = client.post(
        f"{URL_AUTH}/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "test2@example.com", "password": "test1234"}
    )
    headers2 = {"Authorization": f"bearer {response.json()['access_token']}"}

    # Créer category avec utilisateur 1
    create_response = client.post(URL_CATEGORIES, headers=headers1, json=test_category_2)
    category_id = create_response.json()["id"]

    # Essayer d'accéder à la category avec utilisateur 2
    response = client.get(f"{URL_CATEGORIES}/{category_id}/", headers=headers2)
    assert response.status_code == 404

    # Essayer de supprimer la category avec utilisateur 2
    response = client.delete(f"{URL_CATEGORIES}/{category_id}/", headers=headers2)
    assert response.status_code == 404
