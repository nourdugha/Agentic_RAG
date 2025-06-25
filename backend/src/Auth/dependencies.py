from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from typing import Annotated
from src.database.db import SessionLocal
from src.database.tables import Users_tabel
from src.database.models import UserInDB, TokenData
from src.constants import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from src.Auth.security import verify_password
from sqlalchemy.orm import Session

"""
Handles user authentication/validation.
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# get user from DB
def get_user(db:db_dependency, username:str):
    user = db.query(Users_tabel).filter(Users_tabel.username == username).first()
    if user:
        # Convert SQLAlchemy model to dict for Pydantic
        user_dict = {
            "username" : user.username,
            "full_name": user.full_name,
            "email": user.email,
            "is_active":user.is_active,
            "hashed_password": user.hashed_password
        }
        return UserInDB(**user_dict)
    return None

def authenticate_user(db:db_dependency, username:str, password:str):
    user = get_user(db=db, username=username)
    if not user:
        # that means the user is not authenticated
        return False
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        # that means the password not equal to the password in the DB
        return False
    return user


async def get_current_user(db: db_dependency, token:str = Depends(oauth2_scheme)):
    """
    Validates and decodes the JWT token to authenticate the current user.
    
    This function is used as a dependency in protected routes to ensure
    only authenticated users with valid tokens can access them.
    
    Args:
        token (str): The JWT token extracted from the request header using oauth2_scheme
        
    Returns:
        UserInDB: The authenticated user object retrieved from the database
        
    Raises:
        HTTPException: 401 Unauthorized if token validation fails for any reason:
            - Invalid token format
            - Expired token
            - Token signature verification failure
            - Username not found in token payload
            - User not found in database
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get("sub") 
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username) 
    except JWTError:
        raise credentials_exception
    user = get_user(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user:Annotated[UserInDB, Depends(get_current_user)]):
    """
    Verifies that the authenticated user is active in the system.
    
    This function adds an additional layer of validation beyond authentication,
    ensuring that the user not only has valid credentials but is also marked as active
    in the system. It's used for routes that should be accessible only to active users.
    
    Args:
        current_user (UserInDB): The authenticated user object from get_current_user dependency
        
    Returns:
        UserInDB: The authenticated and active user object
        
    Raises:
        HTTPException: 400 Bad Request if the user is not active
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user