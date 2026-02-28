"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from unit_tests.datas import (
    URL_AUTH, URL_USERS, URL_CATEGORIES, URL_BILLS,
    john_doe, login_john_doe, test_bill, test_bill_2,
    test_provider, test_provider_2, john_doe_category
)

def get_auth_headers(client, user_data=login_john_doe):
    """Helper pour obtenir les headers d'authentification"""
    response = client.post(
        f"{URL_AUTH}/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=user_data
    )
    return {"Authorization": f"bearer {response.json()['access_token']}"}

def test_create_bill(client):
    # Créer et connecter utilisateur
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    print(f"Register response: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    current_user = response.json()["current_user"]
    headers = get_auth_headers(client)
    
    # Créer category et provider
    cat_response = client.post(URL_CATEGORIES, headers=headers, json=john_doe_category)
    print(f"Category response: {cat_response.status_code} - {cat_response.json()}")
    category_id = cat_response.json()["id"]
    
    # Créer bill
    bill_data = test_bill.copy()
    bill_data["category_id"] = category_id
    bill_data["provider_id"] = None
    bill_data["user_id"] = current_user["id"]
    print(f"Bill data to send: {bill_data}")
    
    response = client.post(URL_BILLS, headers=headers, json=bill_data)
    print(f"Bill creation response: {response.status_code} - {response.text}")
    
    if response.status_code != 200:
        print(f"Error details: {response.json()}")
    
    assert response.status_code == 200
    bill = response.json()
    print(f"Created bill: {bill}")
    assert bill["title"] == test_bill["title"]
    assert float(bill["amount"]) == float(test_bill["amount"])

def test_get_bills(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    cat_response = client.post(URL_CATEGORIES, headers=headers, json=john_doe_category)
    category_id = cat_response.json()["id"]
    
    # Créer bills
    bill_data = test_bill.copy()
    bill_data["category_id"] = category_id
    client.post(URL_BILLS, headers=headers, json=bill_data)
    
    bill_data2 = test_bill_2.copy()
    bill_data2["category_id"] = category_id
    client.post(URL_BILLS, headers=headers, json=bill_data2)
    
    # Get bills
    response = client.get(URL_BILLS, headers=headers)
    assert response.status_code == 200
    bills = response.json()
    assert len(bills) == 2

def test_get_bill_by_id(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    cat_response = client.post(URL_CATEGORIES, headers=headers, json=john_doe_category)
    category_id = cat_response.json()["id"]
    
    bill_data = test_bill.copy()
    bill_data["category_id"] = category_id
    create_response = client.post(URL_BILLS, headers=headers, json=bill_data)
    bill_id = create_response.json()["id"]
    
    # Get bill by id
    response = client.get(f"{URL_BILLS}/{bill_id}/", headers=headers)
    assert response.status_code == 200
    bill = response.json()
    assert bill["id"] == bill_id

def test_update_bill(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    cat_response = client.post(URL_CATEGORIES, headers=headers, json=john_doe_category)
    category_id = cat_response.json()["id"]
    
    bill_data = test_bill.copy()
    bill_data["category_id"] = category_id
    create_response = client.post(URL_BILLS, headers=headers, json=bill_data)
    bill_id = create_response.json()["id"]
    
    # Update bill
    update_data = {"title": "Facture EDF Modifiée", "amount": 200.0}
    response = client.put(f"{URL_BILLS}/{bill_id}/", headers=headers, json=update_data)
    assert response.status_code == 200
    updated_bill = response.json()
    assert updated_bill["title"] == "Facture EDF Modifiée"
    assert float(updated_bill["amount"]) == 200.0

def test_delete_bill(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    current_user = response.json()["current_user"]
    headers = get_auth_headers(client)
    
    cat_response = client.post(URL_CATEGORIES, headers=headers, json=john_doe_category)
    category_id = cat_response.json()["id"]
    
    bill_data = test_bill.copy()
    bill_data["category_id"] = category_id
    bill_data["user_id"] = current_user["id"]
    create_response = client.post(URL_BILLS, headers=headers, json=bill_data)
    bill_id = create_response.json()["id"]
    
    # Delete bill
    response = client.delete(f"{URL_BILLS}/{bill_id}/", headers=headers)
    assert response.status_code == 200
    
    # Vérifier que la bill n'existe plus
    response = client.get(f"{URL_BILLS}/{bill_id}/", headers=headers)
    assert response.status_code == 404

def test_bill_unauthorized_access(client):
    # Test accès sans authentification
    response = client.get(URL_BILLS)
    assert response.status_code == 401
    
    response = client.post(URL_BILLS, json=test_bill)
    assert response.status_code == 401
