from unit_tests.datas import URL_AUTH, URL_USERS, URL_CATEGORIES
from unit_tests.datas import john_doe, login_john_doe
import pytest

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

    # Verify if default category is created
    # Login
    response = client.post(
        f"{URL_AUTH}/login", 
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=login_john_doe
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    # Check user's categories - should have one default categorie
    response = client.get(URL_CATEGORIES, headers={"Authorization":f"bearer {access_token}"})
    assert response.status_code == 200
    cat = response.json()
    assert len(cat) == 1

