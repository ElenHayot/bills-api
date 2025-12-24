from unit_tests.datas import URL_AUTH, URL_USERS, URL_CATEGORIES, URL_BILLS
from unit_tests.datas import john_doe, login_john_doe, patrick, login_patrick, john_doe_category
import pytest


# Test login a user - create an access_token and a refresh_token
def test_login_user(client):
    # Create a user
    response = client.post(
        URL_USERS,
        json = john_doe
    )
    assert response.status_code == 200

    # Login
    response = client.post(
        f"{URL_AUTH}/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=login_john_doe
    )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] != None
    assert data["refresh_token"] != None

# Test refresh access_token with existing refresh_roken
def test_refresh_user(client):
    # Create a user
    response = client.post(
        URL_USERS,
        json = john_doe
    )
    assert response.status_code == 200

    # Login
    response = client.post(
        f"{URL_AUTH}/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=login_john_doe
    )
    assert response.status_code == 200
    data = response.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    # Then, refresh
    response = client.post(
        f"{URL_AUTH}/refresh",
        headers={"Content-Type": "application/json"},
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] != None
    assert data["refresh_token"] != None
    assert data["access_token"] != access_token

# Test refresh access_token with no refresh_token
def test_refresh_without_token(client):
    response = client.post(
        f"{URL_AUTH}/refresh",
        headers={"Content-Type": "application/json"},
        json={"refresh_token": ""}
    )

    assert response.status_code == 401

# Test get some resources that need authentication
def test_forbidden_access(client):
    response = client.get(URL_CATEGORIES)
    assert response.status_code == 401

    response = client.get(URL_BILLS)
    assert response.status_code == 401

# Test a user can not access another user's sources
def test_user_sources_access(client):
    # Create 2 users
    response = client.post(URL_USERS, json = john_doe)
    assert response.status_code == 200
    response = client.post(URL_USERS, json=patrick)
    assert response.status_code == 200

    # Login 1 user
    response = client.post(
        f"{URL_AUTH}/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=login_john_doe
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    # Create one category
    response = client.post(
        URL_CATEGORIES,
        headers={"Authorization": f"bearer {access_token}"},
        json= john_doe_category
    )
    assert response.status_code == 200

    # Connect second user
    response = client.post(
        f"{URL_AUTH}/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=login_patrick
    )
    assert response.status_code == 200
    access_token_2 = response.json()["access_token"]
    assert access_token != access_token_2

    # Try to get john does's category
    response = client.get(f"{URL_CATEGORIES}/john%20doe%27s%20category", headers={"Authorization": f"bearer {access_token_2}"})
    assert response.status_code == 404

    # Try to delete john doe's category
    response = client.delete(f"{URL_CATEGORIES}/john%20doe%27s%20category", headers={"Authorization": f"bearer {access_token_2}"})
    assert response.status_code == 404


