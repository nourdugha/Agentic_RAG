
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from src.database.models import UserCreate, User, Token, UserInDB
from src.Auth.dependencies import db_dependency, get_current_active_user, authenticate_user, get_user
from src.Auth.security import get_password_hash, create_access_token
from src.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from src.database.tables import Users_tabel

router = APIRouter()


@router.post("/register",response_model=Token)
async def register(user:UserCreate,db:db_dependency):
    """
    Registers a new user by creating a new user record in the database.
    """
    db_user = get_user(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = Users_tabel(username=user.username, full_name=user.full_name, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token(data={"sub":new_user.username})
    return Token(access_token=access_token,token_type="bearer")

@router.post("/token",response_model=Token)
async def login_for_access_token(db: db_dependency, form_data:OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates the user and generates an access token.
    """
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate":"Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username},expires_delta=access_token_expires)
    return {"access_token":access_token,"token_type":"bearer"}

@router.get("/users/me/",response_model=User)
async def read_users_me(current_user:Annotated[UserInDB, Depends(get_current_active_user)]):
    """
    Retrieves the current user's profile information.
    """
    return current_user

@router.get("/users/me/items")
async def read_own_items(current_user:Annotated[UserInDB, Depends(get_current_active_user)]):
    """
    Retrieves the items owned by the current user.
    """
    return [{"item_id":1,"owner":current_user}]










