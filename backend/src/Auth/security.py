from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Optional
from passlib.context import CryptContext
from src.constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

"""
Contains hashing and token creation.
"""


pwd_context = CryptContext(schemes=["bcrypt"])


# to verify the submitted password (plain_one) with hashed one that exist in DB
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

# to hash the password(encrypt)
def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data:dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a JWT access token for authentication.
    
    This function generates a JSON Web Token (JWT) that contains the provided data
    along with an expiration timestamp. The token is signed using the SECRET_KEY
    and the specified algorithm (HS256 by default).
    
    Args:
        data (dict): The payload data to encode in the token, typically contains user information
                    such as username or user ID in the 'sub' field
        expires_delta (timedelta, optional): Custom expiration time for the token.
                    If not provided, defaults to ACCESS_TOKEN_EXPIRE_MINUTES from constants
    
    Returns:
        str: The encoded JWT token as a string
    """
    to_encode = data.copy()
    # Calculate Expiration Time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt