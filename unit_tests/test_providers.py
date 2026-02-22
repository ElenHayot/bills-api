"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from app.auth.auth_schema import RegisterResponse
from unit_tests.datas import (
    URL_AUTH, URL_USERS, URL_PROVIDERS,
    john_doe, login_john_doe, test_provider, test_provider_2
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

def test_create_provider(client):
    # Créer et connecter utilisateur
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    assert response.status_code == 200
    headers = get_auth_headers(client)
    
    # Créer provider
    response = client.post(URL_PROVIDERS, headers=headers, json=test_provider)
    assert response.status_code == 200
    provider = response.json()
    assert provider["name"] == test_provider["name"]

def test_get_providers(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    # Créer plusieurs providers
    client.post(URL_PROVIDERS, headers=headers, json=test_provider)
    client.post(URL_PROVIDERS, headers=headers, json=test_provider_2)
    
    # Get providers
    response = client.get(URL_PROVIDERS, headers=headers)
    assert response.status_code == 200
    providers = response.json()
    assert len(providers) == 2

def test_get_provider_by_id(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    # Créer provider
    create_response = client.post(URL_PROVIDERS, headers=headers, json=test_provider)
    provider_id = create_response.json()["id"]
    
    # Get provider by id
    response = client.get(f"{URL_PROVIDERS}/{provider_id}/", headers=headers)
    assert response.status_code == 200
    provider = response.json()
    assert provider["id"] == provider_id
    assert provider["name"] == test_provider["name"]

def test_update_provider(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    # Créer provider
    create_response = client.post(URL_PROVIDERS, headers=headers, json=test_provider)
    provider_id = create_response.json()["id"]
    
    # Update provider
    update_data = {"name": "EDF Modifié"}
    response = client.put(f"{URL_PROVIDERS}/{provider_id}/", headers=headers, json=update_data)
    assert response.status_code == 200
    updated_provider = response.json()
    assert updated_provider["name"] == "EDF Modifié"

def test_delete_provider(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    # Créer provider
    create_response = client.post(URL_PROVIDERS, headers=headers, json=test_provider)
    provider_id = create_response.json()["id"]
    
    # Delete provider
    response = client.delete(f"{URL_PROVIDERS}/{provider_id}/", headers=headers)
    assert response.status_code == 200
    
    # Vérifier que le provider n'existe plus
    response = client.get(f"{URL_PROVIDERS}/{provider_id}/", headers=headers)
    assert response.status_code == 404

def test_provider_unauthorized_access(client):
    # Test accès sans authentification
    response = client.get(URL_PROVIDERS)
    assert response.status_code == 401
    
    response = client.post(URL_PROVIDERS, json=test_provider)
    assert response.status_code == 401

def test_provider_user_isolation(client):
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

    login_response = response.json()
    access_token = login_response["access_token"]
    headers2 = {"Authorization": f"bearer {access_token}"}

    # Créer provider avec utilisateur 1
    create_response = client.post(URL_PROVIDERS, headers=headers1, json=test_provider)
    provider_id = create_response.json()["id"]

    # Essayer d'accéder au provider avec utilisateur 2
    response = client.get(f"{URL_PROVIDERS}/{provider_id}/", headers=headers2)
    assert response.status_code == 404

    # Essayer de supprimer le provider avec utilisateur 2
    response = client.delete(f"{URL_PROVIDERS}/{provider_id}/", headers=headers2)
    assert response.status_code == 404

def test_provider_pagination(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    # Créer plusieurs providers
    for i in range(5):
        provider_data = {"name": f"Provider {i}", "description": f"Description {i}"}
        client.post(URL_PROVIDERS, headers=headers, json=provider_data)
    
    # Test pagination
    response = client.get(f"{URL_PROVIDERS}?page=1&page_size=2", headers=headers)
    assert response.status_code == 200
    providers = response.json()
    assert len(providers) == 2
    
    response = client.get(f"{URL_PROVIDERS}?page=2&page_size=2", headers=headers)
    assert response.status_code == 200
    providers = response.json()
    assert len(providers) == 2
