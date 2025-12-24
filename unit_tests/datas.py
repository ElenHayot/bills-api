from app.main import API_VERSION

URL_AUTH = f"/api/{API_VERSION}/auth"
URL_USERS = f"/api/{API_VERSION}/users"
URL_CATEGORIES = f"/api/{API_VERSION}/categories"
URL_BILLS = f"/api/{API_VERSION}/bills"

john_doe = {"email": "johndoe@example.com", "password": "jd123PWD"}
login_john_doe = {"username": "johndoe@example.com", "password": "jd123PWD"}
john_doe_category = {"name": "john doe's category", "color": "orange"}

patrick = {"email": "patrick@example.com", "password": "pat123PWD"}
login_patrick = {"username": "patrick@example.com", "password": "pat123PWD"}