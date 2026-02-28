"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from unit_tests.datas import (
    URL_AUTH, URL_USERS, URL_CATEGORIES, URL_BILLS, URL_DASHBOARD, URL_PROVIDERS,
    john_doe, login_john_doe, john_doe_category, test_bill, test_bill_2,
    test_provider
)

def get_auth_headers(client, user_data=login_john_doe):
    """Helper pour obtenir les headers d'authentification"""
    response = client.post(
        f"{URL_AUTH}/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=user_data
    )
    return {"Authorization": f"bearer {response.json()['access_token']}"}

def test_dashboard_basic_stats(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    assert response.status_code == 200
    headers = get_auth_headers(client)
    
    # Créer category et provider
    cat_response = client.post(URL_CATEGORIES, headers=headers, json=john_doe_category)
    category_id = cat_response.json()["id"]
    
    provider_response = client.post(URL_PROVIDERS, headers=headers, json=test_provider)
    provider_id = provider_response.json()["id"]
    
    # Créer quelques bills
    bill_data = test_bill.copy()
    bill_data["category_id"] = category_id
    bill_data["provider_id"] = provider_id
    client.post(URL_BILLS, headers=headers, json=bill_data)
    
    bill_data2 = test_bill_2.copy()
    bill_data2["category_id"] = category_id
    bill_data2["provider_id"] = provider_id
    client.post(URL_BILLS, headers=headers, json=bill_data2)
    
    # Get dashboard stats
    response = client.get(URL_DASHBOARD, headers=headers)
    assert response.status_code == 200
    stats = response.json()
    
    # Vérifier la structure des données
    assert "year" in stats
    assert "currency" in stats
    assert "global_stats" in stats
    assert "by_category" in stats
    
    # Vérifier les valeurs
    assert stats["global_stats"]["nb_bills"] == 2

def test_dashboard_with_year_filter(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    # Créer category
    cat_response = client.post(URL_CATEGORIES, headers=headers, json=john_doe_category)
    category_id = cat_response.json()["id"]
    
    # Créer bill pour 2026
    bill_data = test_bill.copy()
    bill_data["category_id"] = category_id
    bill_data["date"] = "2026-12-20"
    client.post(URL_BILLS, headers=headers, json=bill_data)
    
    # Get dashboard pour 2026
    response = client.get(f"{URL_DASHBOARD}?year=2026", headers=headers)
    assert response.status_code == 200
    stats = response.json()
    assert stats["global_stats"]["nb_bills"] == 1
    
    # Get dashboard pour 2025 (devrait être vide)
    response = client.get(f"{URL_DASHBOARD}?year=2025", headers=headers)
    assert response.status_code == 200
    stats = response.json()
    assert stats["global_stats"]["nb_bills"] == 0

def test_dashboard_unauthorized_access(client):
    # Test accès sans authentification
    response = client.get(URL_DASHBOARD)
    assert response.status_code == 401

def test_dashboard_empty_data(client):
    # Setup utilisateur sans données
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    # Get dashboard vide
    response = client.get(URL_DASHBOARD, headers=headers)
    assert response.status_code == 200
    stats = response.json()
    
    assert float(stats["global_stats"]["nb_bills"]) == float(0)
    assert float(stats["global_stats"]["total_amount"]) == float(0)

def test_dashboard_categories_stats(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    # Créer plusieurs categories
    cat_response = client.post(URL_CATEGORIES, headers=headers, json=john_doe_category)
    cat1_id = cat_response.json()["id"]
    
    cat2_response = client.post(URL_CATEGORIES, headers=headers, json={"name": "Transport", "color": "blue"})
    cat2_id = cat2_response.json()["id"]
    
    # Créer bills dans différentes categories
    bill_data = test_bill.copy()
    bill_data["category_id"] = cat1_id
    client.post(URL_BILLS, headers=headers, json=bill_data)
    
    bill_data2 = test_bill_2.copy()
    bill_data2["category_id"] = cat2_id
    client.post(URL_BILLS, headers=headers, json=bill_data2)
    
    # Get dashboard
    response = client.get(URL_DASHBOARD, headers=headers)
    assert response.status_code == 200
    stats = response.json()
    
    # Vérifier les stats par category
    categories = stats["by_category"]
    assert len(categories) >= 2
    
    # Trouver nos categories dans les résultats
    cat1_stats = next((c for c in categories if c["category_id"] == cat1_id), None)
    cat2_stats = next((c for c in categories if c["category_id"] == cat2_id), None)
    
    assert cat1_stats is not None
    assert cat2_stats is not None
    assert float(cat1_stats["total_amount"]) > 0
    assert float(cat2_stats["total_amount"]) > 0

"""
FOR future feature
def test_dashboard_recent_bills(client):
    # Setup
    response = client.post(f"{URL_USERS}/register/", json=john_doe)
    headers = get_auth_headers(client)
    
    # Créer category
    cat_response = client.post(URL_CATEGORIES, headers=headers, json=john_doe_category)
    category_id = cat_response.json()["id"]
    
    # Créer plusieurs bills
    for i in range(5):
        bill_data = test_bill.copy()
        bill_data["category_id"] = category_id
        bill_data["title"] = f"Bill {i}"
        bill_data["date"] = f"2026-{12-i:02d}-20T00:00:00"
        client.post(URL_BILLS, headers=headers, json=bill_data)
    
    # Get dashboard
    response = client.get(URL_DASHBOARD, headers=headers)
    assert response.status_code == 200
    stats = response.json()
    
    # Vérifier recent bills (limité à N éléments)
    recent_bills = stats["recent_bills"]
    assert len(recent_bills) <= 5  # Doit être limité
    
    # Vérifier que les bills sont triées par date (plus récentes en premier)
    if len(recent_bills) > 1:
        for i in range(len(recent_bills) - 1):
            assert recent_bills[i]["date"] >= recent_bills[i+1]["date"]
"""