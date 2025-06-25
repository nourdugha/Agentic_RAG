from sqlalchemy import Column, Integer, String, Boolean , ForeignKey
from src.database.db import Base

class Users_tabel(Base):
    __tablename__ ="users"
    id = Column(Integer,primary_key=True, index=True)
    username = Column(String,unique=True, index=True)
    full_name = Column(String,unique=True,index=True)
    email = Column(String,unique=True,index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean,default=True)

