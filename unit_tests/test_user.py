"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from unit_tests.datas import URL_AUTH, URL_USERS, URL_CATEGORIES
from unit_tests.datas import john_doe, login_john_doe

def test_create_user(client):
    # Create user
    response = client.post(
        URL_USERS,
        headers={"Content-Type":"application/json"},
        json=john_doe
    )
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == john_doe["email"]

def test_register_user(client):
    # Register user (should return tokens and current_user)
    response = client.post(
        f"{URL_USERS}/register/",
        headers={"Content-Type":"application/json"},
        json=john_doe
    )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] is not None
    assert data["refresh_token"] is not None
    assert data["current_user"]["email"] == john_doe["email"]

    # Verify if default category is created
    access_token = data["access_token"]
    
    # Check user's categories - should have one default category
    response = client.get(URL_CATEGORIES, headers={"Authorization":f"bearer {access_token}"})
    assert response.status_code == 200
    cat = response.json()
    assert len(cat) == 1

def test_get_user_by_id(client):
    # Create user first
    response = client.post(URL_USERS, json=john_doe)
    assert response.status_code == 200
    user_id = response.json()["id"]
    
    # Get user by id
    response = client.get(f"{URL_USERS}/{user_id}/")
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == john_doe["email"]

def test_update_user(client):
    # Create and login user
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    user_id = response.json()["current_user"]["id"]
    
    # Update user
    update_data = {"email": "updated@example.com"}
    response = client.put(
        f"{URL_USERS}/{user_id}/",
        headers={"Authorization": f"bearer {access_token}"},
        json=update_data
    )
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["email"] == "updated@example.com"

def test_delete_user(client):
    # Create and login user
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    user_id = response.json()["current_user"]["id"]
    
    # Delete user
    response = client.delete(
        f"{URL_USERS}/{user_id}/",
        headers={"Authorization": f"bearer {access_token}"}
    )
    assert response.status_code == 200

