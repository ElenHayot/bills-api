"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from app.main import API_PREFIX

URL_AUTH = f"{API_PREFIX}/auth"
URL_USERS = f"{API_PREFIX}/users"
URL_CATEGORIES = f"{API_PREFIX}/categories"
URL_BILLS = f"{API_PREFIX}/bills"
URL_PROVIDERS = f"{API_PREFIX}/providers"
URL_DASHBOARD = f"{API_PREFIX}/dashboard"

john_doe = {"email": "johndoe@example.com", "password": "jd123PWD"}
login_john_doe = {"username": "johndoe@example.com", "password": "jd123PWD"}
john_doe_category = {"name": "john doe's category", "color": "orange"}

patrick = {"email": "patrick@example.com", "password": "pat123PWD"}
login_patrick = {"username": "patrick@example.com", "password": "pat123PWD"}

# Données pour les tests de bills
test_bill = {
    "title": "Facture EDF",
    "amount": 150.5,
    "date": "2026-12-20T00:00:00",
    "category_id": None,  # Sera mis à jour dynamiquement
    "provider_id": None,   # Sera mis à jour dynamiquement
    "provider_name": "",
    "comment": ""
}

test_bill_2 = {
    "title": "Internet Orange",
    "amount": 39.99,
    "date": "2026-12-25T00:00:00",
    "category_id": None,
    "provider_id": None,
    "provider_name": "",
    "comment": ""
}

# Données pour les tests de providers
test_provider = {"name": "EDF"}
test_provider_2 = {"name": "Orange"}

# Données pour les tests de categories
test_category_2 = {"name": "Transport", "color": "blue"}
test_category_3 = {"name": "Alimentation", "color": "green"}