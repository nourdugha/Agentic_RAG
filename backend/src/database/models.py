from pydantic import BaseModel
from typing import Optional,List

class User(BaseModel):
    username : str
    full_name: Optional[str]
    email: Optional[str]

class UserCreate(User):
    password: str

class UserInDB(User):
    hashed_password: str
    is_active: Optional[bool]


class Token(BaseModel):
    access_token : str
    token_type : str

# this data is going to be encoded by our token
class TokenData(BaseModel):
    username: Optional[str] = None