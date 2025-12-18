from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "CHANGE_ME_IN_ENV"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

# Hash a password with bcrypt
def hash_password(password:str) -> str:
    return pwd_context.hash(password)

# Verify password with its hash
def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create a JWT access token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)