from typing import Annotated

from fastapi import APIRouter, Depends
from passlib.handlers.bcrypt import bcrypt
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.util import deprecated

from database import sessionLocal
from models import Users
from passlib.context import CryptContext


router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')





class CreateRequest(BaseModel):
    username:str
    first_name:str
    last_name: str
    email:str
    password:str
    role: str

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]



@router.post("/auth/")
async def create_user(create_user_request:CreateRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    return create_user_model
    # return{'user':'authenticated'}
